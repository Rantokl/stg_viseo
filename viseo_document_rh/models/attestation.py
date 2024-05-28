from odoo import models, fields, api
from odoo.exceptions import ValidationError
import pandas as pd

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

	titre = fields.Many2one('hr.employee', string='Le signataire')



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

	def get_first_date(self):
		self.ensure_one()
		name = self.partner_id.name

		# Préparer la requête SQL de manière sécurisée
		query = """
	           SELECT date_starte 
	           FROM hr_contract 
	           WHERE name = %s
	           ORDER BY date_starte ASC
	           LIMIT 1
	       """

		# Exécuter la requête SQL
		self.env.cr.execute(query, (name,))
		result = self.env.cr.fetchone()

		if result:
			# Convertir le résultat en objet datetime
			date_starte_str = result[0]
			date_starte = datetime.strptime(date_starte_str, '%Y-%m-%d')
			return date_starte.strftime('%d %B %Y')
		return False

	date_begin = fields.Date(compute='get_contract_start_date')
	'''@api.depends('')
	def get_date_begin(self):
		name = self.partner_id.employee_id.name
		date_begin = self.env['hr.contract'].search(['name', '=', name])
		if date_begin:
			df = pd.Dataframe(date_begin)
			df = df.groupby(['date_begin'])
			df = df.iloc[1][1]
			self.date_begin = df.to_Date()'''

	@api.depends('partner_id')
	def get_contract_start_date(self):
		for record in self:
			employee = record.partner_id.employee_id
			if employee:
				contract = self.env['hr.contract'].search([('employee_id', '=', employee.id)], limit=1)
				if contract:
					record.date_begin = contract.date_start
					print(f'$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$${record.date_begin}')
	def print_attestation(self):
		self.get_contract_start_date()
		return {
			'type': 'ir.actions.report',
			'report_name': 'viseo_document_rh.viseo_atestation_template',
			'report_type': 'qweb-pdf',
		}


	