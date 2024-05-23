from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Attestation_travail1(models.Model):
	_name = 'attestation.travail1'	
	_description = 'base supplémentaire pour le certificat de travail'

	partner_id = fields.Many2one('hr.contract',string='Relation:', 
	readonly=True 
	)
	num_sequence = fields.Integer(string='Numéro de Sequence:')
	gender = fields.Selection([
		('Monsieur', 'Monsieur'),
		('Madame', 'Madame'),
		('Mademoiselle', 'Mademoiselle')
	], default='Monsieur')


	actual_year = fields.Date(
	default=lambda self: fields.Date.today()
	)

	actual_year = fields.Date(
			string="Actual Year",
			default=fields.Date.today(),
    )

	formatted_year = fields.Char(
			string="Formatted Year",
			compute='_compute_formatted_year',
			store=True)

	titre = fields.Many2one('hr.employee', string='Le signataire', required=True)


	def _get_formatted_year(self):
			formatted_year = self.actual_year.strftime("%Y")
			return formatted_year

    

	@api.depends('actual_year')
	def _compute_formatted_year(self):
			for record in self:
				record.formatted_year = record._get_formatted_year()

	def check_date_end(self):
			if not self.partner_id.date_end:
				raise ValidationError("La date de fin doit être compléter")



	def print_attestation(self):
		#self.check_date_end()
		return {
			'type': 'ir.actions.report',
			'report_name': 'viseo_document_rh.viseo_atestation_template',
			'report_type': 'qweb-pdf',
		}


	