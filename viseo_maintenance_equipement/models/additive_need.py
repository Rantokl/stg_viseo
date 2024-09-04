from datetime import datetime

from odoo import models, fields, api

class AdditiveDiagBTLine(models.TransientModel):
    _name = 'additive.diag.bt.line'
    _description = 'Diagnostique additive bt'

    name = fields.Char('Lignes de diagnostic')
    additive_need_id = fields.Many2one('additive.need.bt')


class AdditiveNeedBTLine(models.TransientModel):
    _name = 'additive.need.bt.line'
    _description = 'Ligne de besoin additif bt'

    additive_need_id = fields.Many2one('additive.need.bt')
    name = fields.Char(string="Libre")
    product_id = fields.Many2one('product.product', string='Articles')
    product_qty = fields.Float(string="Qté", default=0)
    product_uom = fields.Many2one('uom.uom', related="product_id.uom_id", string="UdM")
    observation = fields.Char(string="OBS")
    maintenance_id = fields.Many2one('maintenance.bike.tools')
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field.")
    operation_done = fields.Char(string="Opérations effectuées")
    time_done = fields.Float(string="Temps passé")
    time_done_unit = fields.Selection(string="Unité de temps",
                                      selection=[('day', 'jours'), ('hour', 'heure'), ('minut', 'minute')],
                                      default='day')
    technician = fields.Many2many('hr.employee', string='Intervenants', copy=False)

class AdditiveNeedBT(models.TransientModel):
    _name = 'additive.need.bt'
    _description = 'Besoin additif bt'

    maintenance_id = fields.Many2one('maintenance.bike.tools', string="Ref maintenance")
    intended_product_ids = fields.One2many('additive.need.bt.line','additive_need_id',string="Liste des pièces")
    diagnostic_lines = fields.One2many('additive.diag.bt.line','additive_need_id',string="Lignes de diagnostic")

    def action_add_need_bt(self):
        self.maintenance_id.notification_rma(u"Besoin additif", 'additive_need')
        self.maintenance_id.update({
            'user_add_need': self.env.user.id,
        })
        self.maintenance_id.update({
            'is_automotive_ok': False,
            'is_pieces_ok': False,
        })

        intended_list = self.env['maintenance.product.list']
        order_line = self.env['maintenance.servicesline']
        diagnostic_line = self.env['maintenance.diagnostic']
        maintenance_id = self.maintenance_id.id

        if self.intended_product_ids:
            intended_list.create({
                'name': 'Besoin additif',
                'display_type': 'line_section',
                'repair_id': maintenance_id,
            })

            order_line.create({
                'name': 'Besoin additif',
                'display_type': 'line_section',
                'id_maintenance': maintenance_id,
            })
        if self.diagnostic_lines:
            diagnostic_line.create({
                'name': 'Besoin additif',
                'display_type': 'line_section',
                'maintenance_id': maintenance_id,
            })
        # print('/////////////////////////////////////////////////' * 4)
        for record in self.intended_product_ids:
            # print('********************'*4)
            # print(record)
            vals = {
                'name': record.name,
                'time_done':record.time_done,
                'time_done_unit': record.time_done_unit,
                'product_id': record.product_id.id,
                'product_qty': record.product_qty,
                'observation': record.observation,
                'repair_id': maintenance_id,
                }
            intended_list.create(vals)

            order_vals = {
                'pieces': record.name,
                'product_uom_qty': record.product_qty,
                'id_maintenance': maintenance_id,
                'price_unit': record.product_id.list_price if record.product_id else 0,
                'name': record.product_id.name,
                'tax_id': record.product_id.taxes_id,
                'product_id': record.product_id.id,
            }
            order_line.create(order_vals)
        for rec in self.diagnostic_lines:
            if rec.name:
                vals = {
                    'name': rec.name,
                    'maintenance_id': maintenance_id,
                }
                diagnostic_line.create(vals)