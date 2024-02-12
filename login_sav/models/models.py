# -*- coding: utf-8 -*-
from odoo import models, fields, api


class login_sav(models.Model):
    # _name = 'login.sav'
#     _description = 'login_sav.login_sav'
    _inherit = 'res.partner'
    login = fields.Char('Login')
    passwd = fields.Char('Password')

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
