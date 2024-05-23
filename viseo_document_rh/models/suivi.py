from odoo import models, api,  fields 


class Suivi_print(models.Model):
	_name = "suivi.print"

	list_champ = []

	def suivi_attestation(self):
		cr = self.env.cr
		query = """
		SELECT * FROM attestation_travail1
		"""
		cr.execute(query)
		results = cr.fetchall()

		# Nettoyer la liste avant d'ajouter de nouveaux éléments
		self.list_champ.clear()

		# Ajouter les résultats à la liste
		for result in results:
			self.list_champ.append(result)

		return {
			'type': 'ir.actions.report',
			'report_name': 'viseo_document_rh.viseo_suivi_attesation_template',
			'report_type': 'qweb-html',	
		}
		
	def suivi_certificat(self):
		cr = self.env.cr

		query = """
		SELECT * FROM certificat_travail
		"""
		cr.execute(query)
		results = cr.fetchall()

		# Nettoyer la liste avant d'ajouter de nouveaux éléments
		self.list_champ.clear()

		# Ajouter les résultats à la liste
		for result in results:
			self.list_champ.append(result)

		return {
			'type': 'ir.actions.report',
			'report_name': 'viseo_document_rh.viseo_suivi_certificat_template',
			'report_type': 'qweb-html',	
		}
		
	def suivi_attestation_provisoire(self):
		pass 