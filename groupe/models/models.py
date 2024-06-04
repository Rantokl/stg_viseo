from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

class PurchaseOrderSI(models.Model):
    _inherit = 'purchase.order'

    _logger = logging.getLogger(__name__)

    #24-05
    import_followup_created = fields.Boolean(string='Import Follow-Up Created', default=False)

    def button_confirm(self):
        res = super(PurchaseOrderSI, self).button_confirm()
        for order in self:
            if order.purchase_type == 'import':
                order.create_import_followup()
                order.import_followup_created = True
                order.redirect_to_import_followup()
        return res
    
    def generate_import_followup_name(self):
        suffix = ''
        if self.company_id.name == 'Ocean Trade':
            suffix = '/OT'
        elif self.company_id.name == 'Continental Auto':
            suffix = '/CA'
        elif self.company_id.name == 'HavaMad':
            suffix = '/HM'
        elif self.company_id.name == 'Izy Rent':
            suffix = '/IZR'
                    
        new_name = '{}{}'.format(self.name, suffix)
        return new_name

    def create_import_followup(self):
            # Find the order line with the highest price_subtotal value
            highest_value_line = max(self.order_line, key=lambda line: line.price_subtotal, default=None)

            if not highest_value_line:
                raise UserError("Aucune ligne de commande trouvée pour ce bon de commande.")

            # Generate the new follow-up name
            new_name = self.generate_import_followup_name()

            # Construct the description of the highest value merchandise
            highest_value_merchandise = "{} {}".format(highest_value_line.product_qty, highest_value_line.product_id.name)
            
            # Create the import follow-up with the new name
            import_followup = self.env['import.followup'].create({
                'name': new_name,
                'purchase_order_in_id': self.id,
                'date_approve': fields.Date.today(),
                'supplier_id': self.partner_id.id,
                #'merchandise': ', '.join("{} {}".format(line.product_qty, line.product_id.name) for line in self.order_line),
                'merchandise': highest_value_merchandise ,
                'amount_total': sum(self.order_line.mapped('price_total')),
                'currency_id': self.currency_id.id,                                
                'incoterm_id': self.incoterm_id.id,
                'supplier_city': self.picking_type_id.warehouse_id.name,
            })
            
            self._logger.info("Created import follow-up: %s", import_followup)
            
            return import_followup

    def redirect_to_import_followup(self):
            return {
                'name': "Import Follow-Up",
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,form',
                'res_model': 'import.followup',
                'domain':[('purchase_order_in_id','=',self.id)],
                'target':'current',
            }


   