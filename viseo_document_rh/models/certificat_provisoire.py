from odoo import models, fields, api
from odoo.exceptions import ValidationError
import pandas as pd


class Provisoire_RH(models.Model):
	_name = 'provisoire.docrh'	
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
	#job_titles = []
	'''
	job_department = []
	date_start = []
	date_end = []
	test_1 = []'''

	@api.model
	def get_contract_job_titles(self):

		'''save = self.env['hr.contract'].browse(type_id_id)

		save = self.env['hr.contract'].browse(type_id)

		cr = self.env.cr
		#name_id = self.env.context.get('partner_id', False)
		#contract = self.env['hr.contract'].browse(name_id)
		name_id = self.partner_id.name

		query = """
		SELECT
            c.date_start,
            c.date_end,
            j.name AS job_title,
            d.name AS department,
			g.name AS category
        FROM
            hr_contract c
        INNER JOIN
            hr_job j ON c.job_id = j.id
        INNER JOIN
            hr_department d ON c.department_id = d.id
		INNER JOIN
			hr_employee_category g ON c.type_id_id = g.id
        WHERE
            c.name = %s
			"""

		cr.execute(query, (name_id,))

		results = cr.fetchall()
		for result in results:
				if result not in self.job_titles:
					if result[1] and result[0]:
						self.job_titles.append(result)
				#self.date_start.append(results[i][0])
				#self.date_end.append(results[i][1])
				#self.job_department.append(results[i][3])

		query2 = " SELECT name from hr_job where id = %s"
		cr.execute(query2, (test,))
		results2 = cr.fetchall()
		for i in range(len(results2)):
			self.test_1.append(results2[i])'''

		
		'''if contract:
			self.job_titles.append({
				'date_start': contract.date_start,
				'date_end': contract.date_end,
				'job_title': contract.job_id.name if contract.job_id else False,
				'department': contract.department_id.name if contract.department_id else False,
				
			})	

		contract_data = []
		name_id = self.partner_id.name

		contracts = self.env['hr.contract'].search([('name', '=', name_id)])
		for contract in contracts:
			date_start = contract.date_start
			date_end = contract.date_end
			job_title = contract.job_id.name
			department = contract.department_id.name
			# Pour accéder au champ calculé type_id, vous pouvez simplement l'appeler comme n'importe quel autre champ
			category = contract.type_id.name

			contract_data = [date_start, date_end, job_title, department, category]

			# Check if contract_data is not already in self.results
			if contract_data not in results:
				# Check if the first two elements of contract_data are truthy
				if contract_data[0] and contract_data[1]:	
						
					# Check if the tuple with the same job_title, department, and category is not already present in self.results
						if all((contract_data[2], contract_data[3], contract_data[4]) != (result[2], result[3], result[4]) for result in results):
							results.append(contract_data)
		return results

	def get_contract_job_titles_shadow(self, results_shadow):

		contract_data_shadow = []
		name_id_shadow = self.partner_id.name
		compteur = 0

		contracts_shadow = self.env['hr.contract'].search([('name', '=', name_id_shadow)])
		for contract in reversed(contracts_shadow):
			
			date_start_shadow = contract.date_start
			date_end_shadow = contract.date_end
			job_title_shadow  = contract.job_id.name
			department_shadow  = contract.department_id.name
			# Pour accéder au champ calculé type_id, vous pouvez simplement l'appeler comme n'importe quel autre champ
			category_shadow = contract.type_id.name

			contract_data_shadow  = [date_start_shadow , date_end_shadow , job_title_shadow , department_shadow , category_shadow]	
			if contract_data_shadow  not in results_shadow:
				# Check if the first two elements of contract_data are truthy
				if contract_data_shadow[0] and contract_data_shadow[1]:	
						
					# Check if the tuple with the same job_title, department, and category is not already present in self.results
						if all((contract_data_shadow[2], contract_data_shadow[3], contract_data_shadow[4]) != (result[2], result[3], result[4]) for result in results_shadow):
							compteur = compteur + 1 
							results_shadow.append(contract_data_shadow)			
		return results_shadow'''

		

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



	def print_certificat_provisoire(self):
		self.get_contract_job_titles()
		self.check_date_end()
		return {
			'type': 'ir.actions.report',
			'report_name': 'viseo_document_rh.viseo_certificat_provisoire_template',
			'report_type': 'qweb-pdf',
			
		}
