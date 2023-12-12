#-*- coding: utf-8 -*-

from odoo import models, fields, api


class devis_pdf_vente(models.Model):
	_inherit = 'sale.order.line'

	def get_vehicle_model(self):
		for rec in self:
			if rec.product_id:
				model_vehicle = self.env['fleet.vehicle'].search([('model_id', '=', rec.product_id.model_id.name)])
				print('"""""""""""""""""')
				# print(model_vehicle[1][1])
				print()

				return rec.product_id.model_id.name




