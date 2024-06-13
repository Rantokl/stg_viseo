# -*- coding:utf-8 -*-

from odoo import fields, api, models
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    bypass_vin_sale = fields.Boolean(default=False,copy=False,track_visibility=True)

    # def write(self, vals):
    #     res = super(SaleOrder,self).write(vals)
    #     if 'state' in vals:
    #         if vals['state'] == 'sale':
    #             veh_qty = 0
    #             # sale_order = self.env['sale.order'].search([('name', '=', self.invoice_origin)])
    #             for sales in filter(lambda x: x.product_id.model_id, self.order_line): veh_qty += sales.product_uom_qty
    #             if veh_qty >= 1:
    #                 if (self.vehicle_ids is None) and not self.bypass_vin_sale:
    #                     raise ValidationError(('Ajouter le(s) VIN de véhicule(s) dans la vente'))
    #                 else:
    #                     if veh_qty != len(self.vehicle_ids) and not self.bypass_vin_sale:
    #                         raise ValidationError(('Ajuster le nombre de véhicule suivant la commande dans le vente'))
    #     return res

    def action_confirm(self):
        veh_qty=0
        # sale_order = self.env['sale.order'].search([('name', '=', self.invoice_origin)])
        for sales in filter(lambda x: x.product_id.model_id, self.order_line): veh_qty += sales.product_uom_qty
        if veh_qty >= 1:
            if (self.vehicle_ids is None) and not self.bypass_vin_sale:
                raise ValidationError("Veuillez ajouter les VIN dans l'onglet véhicule")
            else:
                if veh_qty != len(self.vehicle_ids) and not self.bypass_vin_sale:
                    raise ValidationError("Veuillez ajuster les VIN par rapport à la quantité commandée dans l'onglet véhicule.")
        return super(SaleOrder, self).action_confirm()

    def action_bypass_vin(self):
        for rec in self:
            rec.update({
                'bypass_vin_sale': True
            })