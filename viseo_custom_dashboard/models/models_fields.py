# -*- coding: utf-8 -*-
import json
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import ValidationError, UserError
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from pprint import pprint

class viseo_custom_DashboardNinjaItems(models.Model):
	_inherit = "ks_dashboard_ninja.item"
	_description = 'Custom dashboard ninja for VISEO'

	ks_dashboard_item_type = fields.Selection([
		('ks_tile', 'Tile'),
		('ks_bar_chart_many', 'Bar Chart (Multi modèles)'),
		('ks_bar_chart', 'Bar Chart'),
		('ks_horizontalBar_chart', 'Horizontal Bar Chart'),
		('ks_line_chart', 'Line Chart'),
		('ks_area_chart', 'Area Chart'),
		('ks_pie_chart', 'Pie Chart'),
		('ks_doughnut_chart', 'Doughnut Chart'),
		('ks_polarArea_chart', 'Polar Area Chart'),
		('ks_list_view', 'List View'),
		('ks_kpi', 'KPI')
	],
	default=lambda self: self._context.get('ks_dashboard_item_type', 'ks_tile'),
	required=True,
	string="Dashboard Item Type")

	ks_monetary_unit_1_many = fields.Boolean(string="Unité monétaire", default=False)
	ks_monetary_unit_2_many = fields.Boolean(string="Unité monétaire", default=False)

	ks_field_1_name = fields.Char(string='Nom')
	ks_model_id_1_many = fields.Many2one('ir.model', string='Modèles 1 (bar)',
		domain="[('access_ids','!=',False),('transient','=',False),"
				"('model','not ilike','base_import%'),('model','not ilike','ir.%'),"
				"('model','not ilike','web_editor.%'),('model','not ilike','web_tour.%'),"
				"('model','!=','mail.thread'),('model','not ilike','ks_dash%')]")
	ks_domain_many_1 = fields.Char(string="Domaine many 1")
	ks_model_name_many_1 = fields.Char(related='ks_model_id_1_many.model', string="Model Name 1")
	ks_chart_data_count_type_many_1 = fields.Selection([
		('count', 'Nombre'),
		('sum', 'Somme'),
		('average', 'Moyenne')],
		string="Type 1", default="sum")

	ks_date_filter_field_many_1 = fields.Many2one('ir.model.fields',
		domain="[('model_id','=',ks_model_id_1_many),'|',('ttype','=','date'),"
				"('ttype','=','datetime')]",
		string="Filtrer par Date 1")
	@api.onchange('ks_model_id_1_many')
	def ks_date_filter_field_delault_value(self):
		for rec in self:
			# To show "created on" by default on date filter field on model select.
			if rec.ks_model_id_1_many:
				datetime_field_list = rec.ks_date_filter_field_many_1.search(
					[('model_id', '=', rec.ks_model_id_1_many.id), '|', ('ttype', '=', 'date'),
						('ttype', '=', 'datetime')]).read(['id', 'name'])
				for field in datetime_field_list:
					if field['name'] == 'create_date':
						rec.ks_date_filter_field_many_1 = field['id']
			else:
				rec.ks_date_filter_field_many_1 = False


	ks_field_2_name = fields.Char(string='Nom')
	ks_model_id_2_many = fields.Many2one('ir.model', string='Modèles 2 (ligne)',
		domain="[('access_ids','!=',False),('transient','=',False),"
				"('model','not ilike','base_import%'),('model','not ilike','ir.%'),"
				"('model','not ilike','web_editor.%'),('model','not ilike','wesb_tour.%'),"
				"('model','!=','mail.thread'),('model','not ilike','ks_dash%')]")
	ks_domain_many_2 = fields.Char(string="Domaine many 2")
	ks_model_name_many_2 = fields.Char(related='ks_model_id_2_many.model', string="Model Name")
	ks_chart_data_count_type_many_2 = fields.Selection([
		('count', 'Nombre'),
		('sum', 'Somme'),
		('average', 'Moyenne')],
		string="Type 2", default="sum")

	ks_date_filter_field_many_2 = fields.Many2one('ir.model.fields',
		domain="[('model_id','=',ks_model_id_2_many),'|',('ttype','=','date'),"
				"('ttype','=','datetime')]",
		string="Filtrer par Date 2")
	@api.onchange('ks_model_id_2_many')
	def ks_date_filter_field_delault_value_2(self):
		for rec in self:
			# To show "created on" by default on date filter field on model select.
			if rec.ks_model_id_2_many:
				datetime_field_list = rec.ks_date_filter_field_many_2.search(
					[('model_id', '=', rec.ks_model_id_2_many.id), '|', ('ttype', '=', 'date'),
						('ttype', '=', 'datetime')]).read(['id', 'name'])
				for field in datetime_field_list:
					if field['name'] == 'create_date':
						rec.ks_date_filter_field_many_2 = field['id']
			else:
				rec.ks_date_filter_field_many_2 = False


	ks_domain_many_3 = fields.Char(string="Domaine many 3")


	ks_chart_measure_field_many = fields.Many2many('ir.model.fields', 'ks_dn_measure_field_many_rel', 'measure_field_id', 'field_id',
		domain="[('model_id','=',ks_model_id_1_many),('name','!=','id'),"
				"('store','=',True),'|','|',"
				"('ttype','=','integer'),('ttype',	'=','float'),"
				"('ttype','=','monetary')]",
		string="Measure model 1")

	ks_chart_measure_field_2_many = fields.Many2many('ir.model.fields', 'ks_dn_measure_field_many_rel_2', 'measure_field_id_2', 'field_id',
		domain="[('model_id','=',ks_model_id_2_many),('name','!=','id'),"
			"('store','=',True),'|','|',"
			"('ttype','=','integer'),('ttype','=','float'),"
			"('ttype','=','monetary')]",
		string="Measure model 2")


	ks_chart_relation_groupby_many = fields.Many2one('ir.model.fields',
		domain="['|',('model_id','=',ks_model_id_1_many),('model_id','=',ks_model_id_2_many),"
			"('name','!=','id'),"
			"('store','=',True),'|',('ttype','=','many2one'),('ttype','=','monetary')]",
		string="Groupé par ")

	# *****************************************************************************

	# @api.depends('ks_chart_relation_groupby')
	
	ks_model_id = fields.Many2one('ir.model', string='Modèle',
		domain="[('access_ids','!=',False),('transient','=',False),"
				"('model','not ilike','base_import%'),('model','not ilike','ir.%'),"
				"('model','not ilike','web_editor.%'),('model','not ilike','web_tour.%'),"
				"('model','!=','mail.thread'),('model','not ilike','ks_dash%')]")
	
	ks_chart_relation_groupby = fields.Many2one('ir.model.fields',
		domain="[('model_id','=',ks_model_id),('name','!=','id'),"
				"('store','=',True),('ttype','!=','binary'),"
				"('ttype','!=','many2many'), ('ttype','!=','one2many')]",
		string="Groupé par")


	ks_chart_measure_field_count = fields.Many2one('ir.model.fields',
		# domain=lambda self: self._compute_domain_bla(),
		domain="[('model_id', '=', ks_chart_relation_groupby.relation.model_id)]",
		# compute='_compute_ks_chart_measure_field_count',
		string="Groupé par ")


	def _compute_domain_bla(self):
		if self.ks_chart_relation_groupby.relation:
			model_name = self.ks_chart_relation_groupby.relation
			model_id = self.env['ir.model'].search([('model', '=', model_name)], limit=1)

			model_count = [
				('model_id', '=', model_id)
			]
			return model_count


	@api.depends('ks_chart_relation_groupby')
	def _compute_ks_chart_measure_field_count(self):
		for record in self:
			if record.ks_chart_relation_groupby:
				related_model = record.ks_chart_relation_groupby.relation
				if related_model:
					model_id = self.env['ir.model'].search([('model', '=', related_model)], limit=1)
					if model_id:
						fields = self.env['ir.model.fields'].search([('model_id', '=', model_id.id)])
						record.ks_chart_measure_field_count = fields and fields.ids or False
					else:
						record.ks_chart_measure_field_count = False
				else:
					record.ks_chart_measure_field_count = False
			else:
				record.ks_chart_measure_field_count = False



	@api.onchange('ks_chart_relation_groupby')
	def print_domain(self):
		for rec in self:
			print()
			print()
			print()
			print(rec.ks_model_id)
			print(rec.ks_model_id.name)
			print()
			print(rec.ks_chart_relation_groupby.model_id)
			# print(rec.ks_chart_relation_groupby.relation.model_id)
			print(rec.env['ir.model'].search([('model', '=', rec.ks_chart_relation_groupby.relation)], limit=1))
			print(rec.env['ir.model'].search([('model', '=', rec.ks_chart_relation_groupby.relation)], limit=1).name)
			print()
			if rec.ks_chart_relation_groupby.relation:
				model_name = rec.ks_chart_relation_groupby.relation
				model_id = rec.env['ir.model'].search([('model', '=', model_name)], limit=1)
				# pprint(model_id.fields_get())
				pprint(model_id.fields_get_keys())
				print()
				model_count = [
					('id', '=', model_id.id)
				]
				# pprint(model_count)
				fields = rec.env['ir.model'].search(model_count, limit=1)
				pprint(fields)
			print()
			print()
			print()



	# *****************************************************************************


	ks_chart_groupby_many_type = fields.Char(compute='get_chart_groupby_many_type',compute_sudo=False)
	@api.depends('ks_chart_relation_groupby_many')
	def get_chart_groupby_many_type(self):
		for rec in self:
			if rec.ks_chart_relation_groupby_many.ttype == 'datetime' or rec.ks_chart_relation_groupby_many.ttype == 'date':
				rec.ks_chart_groupby_many_type = 'date_type'
			elif rec.ks_chart_relation_groupby_many.ttype == 'many2one':
				rec.ks_chart_groupby_many_type = 'relational_type'
			elif rec.ks_chart_relation_groupby_many.ttype == 'selection':
				rec.ks_chart_groupby_many_type = 'selection'
			else:
				rec.ks_chart_groupby_many_type = 'other'

	

	ks_sort_by_field_many = fields.Many2one('ir.model.fields',
		domain="['|',('model_id','=',ks_model_id_1_many),('model_id','=',ks_model_id_2_many),"
				"('name','!=','id'),('store','=',True),('ttype','=','many2one')]",
		string="Trié par (many)")

	ks_show_gridlines = fields.Boolean(string="Afficher lignes", default=True)

	ks_chart_x_axe_font_size = fields.Integer(default=12)
	ks_chart_y_axe_font_size = fields.Integer(default=12)
	ks_chart_legend_font_size = fields.Integer(default=12)
	ks_chart_title_font_size = fields.Integer(string="Taille de police (Pt)", default=12)

	ks_chart_measure_field_name_1_1 = fields.Char(string='mesure 1', default=False)
	ks_chart_measure_field_name_1_2 = fields.Char(string='mesure 2', default=False)
	ks_chart_measure_field_name_1_3 = fields.Char(string='mesure 3', default=False)
	ks_chart_measure_field_name_1_4 = fields.Char(string='mesure 4', default=False)

	ks_chart_measure_field_name_2_1 = fields.Char(string='mesure 1', default=False)
	ks_chart_measure_field_name_2_2 = fields.Char(string='mesure 2', default=False)
	ks_chart_measure_field_name_2_3 = fields.Char(string='mesure 3', default=False)
	ks_chart_measure_field_name_2_4 = fields.Char(string='mesure 4', default=False)

		


	@api.onchange('ks_model_id_1_many')
	def empty_field_model_many_1(self):
		for rec in self:
			if rec.ks_domain_many_1:
				rec.ks_domain_many_1 = False
			if rec.ks_domain_many_3:
				rec.ks_domain_many_3 = False
			if rec.ks_sort_by_field_many:
				rec.ks_sort_by_field_many = False
			if rec.ks_date_filter_field_many_1:
				rec.ks_date_filter_field_many_1 = False
			if rec.ks_chart_measure_field_many:
				rec.ks_chart_measure_field_many = False
			if rec.ks_chart_relation_groupby_many:
				rec.ks_chart_relation_groupby_many = False


	@api.onchange('ks_model_id_2_many')
	def empty_field_model_many_2(self):
		for rec in self:
			if rec.ks_domain_many_2:
				rec.ks_domain_many_2 = False
			if rec.ks_domain_many_3:
				rec.ks_domain_many_3 = False
			if rec.ks_sort_by_field_many:
				rec.ks_sort_by_field_many = False
			if rec.ks_date_filter_field_many_2:
				rec.ks_date_filter_field_many_2 = False
			if rec.ks_chart_measure_field_2_many:
				rec.ks_chart_measure_field_2_many = False
			if rec.ks_chart_relation_groupby_many:
				rec.ks_chart_relation_groupby_many = False


	@api.onchange('ks_chart_measure_field_many')
	def change_ks_chart_measures_many_name(self):
		
		if len(self.ks_chart_measure_field_many) > 4:
			raise ValidationError(f'You can only select up to 4 values.')
		
		for rec in self:
			if rec.ks_chart_measure_field_many:
				values = []
				for name in rec.ks_chart_measure_field_many:
					values.append(name.field_description)

				rec.ks_chart_measure_field_name_1_1 = values[0] if values else False
				rec.ks_chart_measure_field_name_1_2 = values[1] if len(values) > 1 else False
				rec.ks_chart_measure_field_name_1_3 = values[2] if len(values) > 2 else False
				rec.ks_chart_measure_field_name_1_4 = values[3] if len(values) > 3 else False
			else:
				rec.ks_chart_measure_field_name_1_1 = False


	@api.onchange('ks_chart_measure_field_2_many')
	def change_ks_chart_measures_2_many_name(self):
		
		if len(self.ks_chart_measure_field_2_many) > 4:
			raise ValidationError(f'You can only select up to 4 values.')

		for rec in self:
			if rec.ks_chart_measure_field_2_many:
				values = []
				for name in rec.ks_chart_measure_field_2_many:
					values.append(name.field_description)

				rec.ks_chart_measure_field_name_2_1 = values[0] if values else False
				rec.ks_chart_measure_field_name_2_2 = values[1] if len(values) > 1 else False
				rec.ks_chart_measure_field_name_2_3 = values[2] if len(values) > 2 else False
				rec.ks_chart_measure_field_name_2_4 = values[3] if len(values) > 3 else False
			else:
				rec.ks_chart_measure_field_name_2_1 = False


	@api.onchange('ks_chart_data_count_type_many_1')
	def empty_chart_measures_name_1(self):
		for rec in self:
			if rec.ks_chart_data_count_type_many_1 == 'count' and rec.ks_dashboard_item_type == 'ks_bar_chart_many':
				rec.ks_chart_measure_field_name_1_1 = "Nombre de " + rec.ks_model_id_1_many.name
				rec.ks_chart_measure_field_many = False
				rec.ks_chart_measure_field_name_1_2 = False
				rec.ks_chart_measure_field_name_1_3 = False
				rec.ks_chart_measure_field_name_1_4 = False
			else :
				rec.ks_chart_measure_field_name_1_1 = False


	@api.onchange('ks_chart_data_count_type_many_2')
	def empty_chart_measures_name_2(self):
		for rec in self:
			if rec.ks_chart_data_count_type_many_2 == 'count' and rec.ks_dashboard_item_type == 'ks_bar_chart_many':
				rec.ks_chart_measure_field_name_2_1 = "Nombre de " + rec.ks_model_id_2_many.name
				rec.ks_chart_measure_field_many = False
				rec.ks_chart_measure_field_name_2_2 = False
				rec.ks_chart_measure_field_name_2_3 = False
				rec.ks_chart_measure_field_name_2_4 = False
			else :
				rec.ks_chart_measure_field_name_2_1 = False


	@api.onchange('ks_chart_measure_field')
	def change_ks_chart_measures_name(self):
		for rec in self:
			if rec.ks_chart_measure_field:
				values = []
				for name in rec.ks_chart_measure_field:
					values.append(name.field_description)

				rec.ks_chart_measure_field_name_1_1 = values[0] if values else False
				rec.ks_chart_measure_field_name_1_2 = values[1] if len(values) > 1 else False
				rec.ks_chart_measure_field_name_1_3 = values[2] if len(values) > 2 else False
				rec.ks_chart_measure_field_name_1_4 = values[3] if len(values) > 3 else False
			else:
				rec.ks_chart_measure_field_name_1_1 = False


	@api.onchange('ks_chart_measure_field_2')
	def change_ks_chart_measures_name_2(self):
		for rec in self:
			if rec.ks_chart_measure_field_2:
				values_2 = []
				for name in rec.ks_chart_measure_field_2:
					values_2.append(name.field_description)

				rec.ks_chart_measure_field_name_2_1 = values_2[0] if values_2 else False
				rec.ks_chart_measure_field_name_2_2 = values_2[1] if len(values_2) > 1 else False
				rec.ks_chart_measure_field_name_2_3 = values_2[2] if len(values_2) > 2 else False
				rec.ks_chart_measure_field_name_2_4 = values_2[3] if len(values_2) > 3 else False
			else:
				rec.ks_chart_measure_field_name_2_1 = False


	@api.onchange('ks_chart_data_count_type')
	def empty_ks_chart_measures_name(self):
		for rec in self:
			if rec.ks_chart_data_count_type == 'count' and rec.ks_dashboard_item_type != 'ks_bar_chart_many':
				rec.ks_chart_measure_field_name_1_1 = "Nombre de " + rec.ks_model_id.name
				rec.ks_chart_measure_field = False
				rec.ks_chart_measure_field_name_1_2 = False
				rec.ks_chart_measure_field_name_1_3 = False
				rec.ks_chart_measure_field_name_1_4 = False

				if rec.ks_dashboard_item_type == 'ks_bar_chart':
					rec.ks_chart_measure_field_2 = False
					rec.ks_chart_measure_field_name_2_1 = False
					rec.ks_chart_measure_field_name_2_2 = False
					rec.ks_chart_measure_field_name_2_3 = False
					rec.ks_chart_measure_field_name_2_4 = False
			else:
				rec.ks_chart_measure_field_name_1_1 = False
				rec.ks_chart_measure_field_name_2_1 = False	



class viseo_custom_KsDashboardItemsActions(models.Model):
	_inherit = "ks_dashboard_ninja.item_action"
	_description = 'Dashboard Ninja Items Goal Lines'

	ks_dashboard_item_id_many = fields.Many2one('ks_dashboard_ninja.item', string="Dashboard Item")
	ks_model_id_1_many = fields.Many2one('ir.model', related='ks_dashboard_item_id_many.ks_model_id_1_many')
	ks_model_id_2_many = fields.Many2one('ir.model', related='ks_dashboard_item_id_many.ks_model_id_2_many')









