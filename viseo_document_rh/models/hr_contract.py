from odoo import models, fields, api


class Hr_contract_inherit(models.Model):		
		_inherit = ['hr.contract']
		

		type_id_id = fields.Many2one('hr.employee.category', stored=True)
