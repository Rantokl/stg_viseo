from odoo import models, api, fields

class Logo(models.Model):
	_inherit = ['res.company']



	capital = fields.Char(string="Capital")
	