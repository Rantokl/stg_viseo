# -*- coding: utf-8 -*-

from odoo import models, fields, api





class viseo_rfid(models.Model):
    _name = 'fleet.viseo.vehicule.logs'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Véhicule")
    id_vehicle = fields.Char(string='ID Vehicle', visible=False)
    vehicle = fields.Char(string='Vehicle')
    tag_rfid = fields.Many2one('viseo.tag.rfid',track_visibility='always',  string='Tag rfid')
    rfid_tag = fields.Char(string='Tag rfid')
    date_check = fields.Char(string="Check-in")
    location = fields.Char(string="Location")

    #_inherit = 'fleet.vehicle'


    @api.model
    def create(self, values):

        new_record = super(viseo_rfid, self).create(values)

        return new_record

    # def open_vehicle_logs(self):
    #     self.ensure_one()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Historique des vehicules',
    #         'view_mode': 'tree',
    #         'res_model': 'fleet.viseo.vehicule.logs',
    #         #'domain': [('vehicle_id', '=', self.id)],
    #         #'context': {'default_driver_company': self.true_driver.id, 'default_driver_other': self.other_driver, 'default_vehicle_id': self.id}
    #     }
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100



