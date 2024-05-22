from odoo import models, fields, api
from odoo.exceptions import ValidationError
import numpy as np
import pandas as pd





class Attestation_travail(models.Model):
	_name = 'certificat.travail'
	_description = 'base supplémentaire pour le certificat de travail'

	partner_id = fields.Many2one('hr.contract',string='Relation:', 
	readonly=True 
	)
	#employee_id = fields.Many2one('hr.contract', default='employee_id')
	num_sequence = fields.Integer(string='Numéro de Sequence:', required=True)
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

	
	get_data = fields.Char(
		string='Data to print',
	)
	titre = fields.Many2one('hr.employee', string='Le signataire', required=True)

	get_date_end = []

	titre_post = []


	@api.model
	def get_contract_job_titles(self):

		name_id = self.partner_id.name
		contracts = self.env['hr.contract'].search([('name', '=', name_id)])

		data = []
		for contract in contracts:
			date_start = contract.date_start
			date_end = contract.date_end
			job_title = contract.job_id.name
			department = contract.department_id.name
			category = contract.type_id.name
			data.append([date_start, date_end, job_title, department, category])

		df = pd.DataFrame(data, columns=['Date Start', 'Date End', 'Job Title', 'Department', 'Category'])
		self.titre_post.clear()
		df_max_dates = df.groupby(['Job Title', 'Department', 'Category'])['Date End'].max().reset_index()
		df_max_dates_dict = df_max_dates.to_dict(orient='records')
		
		for i in df_max_dates_dict:
			self.titre_post.append(i)
		self.titre_post



		# Assigning df_str to selfs.get_data
		self.get_date_end.clear()
		df_min_dates =  df.groupby(['Job Title', 'Department', 'Category'])['Date Start'].min().reset_index()
		df_min_dates_dict = df_min_dates.to_dict(orient='records')

		
		for x in df_min_dates_dict:
			self.get_date_end.append(x)
		self.get_date_end

	def _get_formatted_year(self):
			formatted_year = self.actual_year.strftime("%Y")
			return formatted_year

    

	@api.depends('actual_year')
	def _compute_formatted_year(self):
			for record in self:
				record.formatted_year = record._get_formatted_year()

	def check_date_end(self):
			if not self.partner_id.date_end:
				raise ValidationError("La date de fin doit être complété")



	def print_certificat(self):
		self.check_date_end()
		self.get_contract_job_titles()
		return {
			'type': 'ir.actions.report',
			'report_name': 'viseo_document_rh.viseo_certificat_template',
			'report_type': 'qweb-pdf',	
		}
