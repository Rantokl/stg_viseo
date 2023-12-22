
# -*- coding: utf-8 -*-
import dateutil
import datetime as dt
import pytz
import json
import babel

from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from collections import defaultdict
from datetime import datetime
from dateutil import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.addons.ks_dashboard_ninja.lib.ks_date_filter_selections import ks_get_date
from pprint import pprint
import ast
from collections import defaultdict

class viseo_custom_DashboardNinjaItems(models.Model):
	_inherit = "ks_dashboard_ninja.item"

	@api.depends('ks_chart_measure_field', 'ks_chart_relation_groupby','ks_model_id','ks_chart_measure_field_2','ks_chart_relation_sub_groupby','ks_chart_date_sub_groupby',
					'ks_chart_measure_field_many','ks_model_id_1_many',
					'ks_chart_measure_field_2_many','ks_model_id_2_many', 'ks_chart_relation_groupby_many',
					'ks_chart_date_groupby', 'ks_domain',
					'ks_dashboard_item_type',  'ks_sort_by_field', 'ks_sort_by_order',
					'ks_record_data_limit', 'ks_chart_data_count_type',  'ks_goal_enable',
					'ks_standard_goal_value', 'ks_goal_bar_line', 
					'ks_date_filter_field', 'ks_item_start_date', 'ks_item_end_date',
					'ks_compare_period', 'ks_year_period', 'ks_unit', 'ks_unit_selection', 'ks_chart_unit')
	def ks_get_chart_data(self):
		for rec in self:
			final_data = None

			if rec.ks_dashboard_item_type and rec.ks_dashboard_item_type == 'ks_bar_chart_many' and \
				rec.ks_model_id_1_many and rec.ks_model_id_2_many and rec.ks_chart_data_count_type_many_1 and rec.ks_chart_data_count_type_many_2:

				ks_chart_data_1 = {
					'labels': [],
					'datasets': [],
					'ks_currency': 0,
					'ks_field': "",
					'ks_selection': "",
					'ks_show_second_y_scale': True,
					'domains': [],
				}

				ks_chart_data_2 = {
					'labels': [],
					'datasets': [],
					'ks_currency': 0,
					'ks_field': "",
					'ks_selection': "",
					'ks_show_second_y_scale': True, 
					'domains': [],
				}

				ks_chart_measure_field_many = []
				ks_chart_measure_field_many_ids = []
				ks_chart_measure_field_2_many = []
				ks_chart_measure_field_2_ids_many = []

				data_set_2 = []
				data_set_1 = []

				if rec.ks_chart_data_count_type_many_1 == "count":
					ks_chart_data_1['datasets'].append({'data': [], 'label': rec.ks_model_id_1_many.name})
					data_set_1.append({'data': [], 'label': rec.ks_model_id_1_many.name})
				else:
					for res in rec.ks_chart_measure_field_many:
						ks_chart_measure_field_many.append(res.name)
						ks_chart_measure_field_many_ids.append(res.id)
						ks_chart_data_1['datasets'].append({'data': [], 'label': res.field_description})
						data_set_1.append({'data': [], 'label': res.field_description})

				if rec.ks_chart_data_count_type_many_2 == "count":
					ks_chart_data_2['datasets'].append({'data': [], 'label': rec.ks_model_id_2_many.name, 'type': 'line', 'yAxisID': 'y-axis-1'})
					data_set_2.append({'data': [], 'label': rec.ks_model_id_2_many.name, 'type': 'line', 'yAxisID': 'y-axis-1'})
				else:
					for res in rec.ks_chart_measure_field_2_many:
						ks_chart_measure_field_2_many.append(res.name)
						ks_chart_measure_field_2_ids_many.append(res.id)
						ks_chart_data_2['datasets'].append({'data': [], 'label': res.field_description, 'type': 'line', 'yAxisID': 'y-axis-1'})
						data_set_2.append({'data': [], 'label': res.field_description, 'type': 'line', 'yAxisID': 'y-axis-1'})


				ks_chart_groupby_relation_field_many = rec.ks_chart_relation_groupby_many.name

				ks_chart_domain_many_1 = self.compute_same_domain_many(rec.ks_domain_many_1, rec.ks_domain_many_3, rec.ks_date_filter_field_many_1, ks_chart_groupby_relation_field_many, rec)
				ks_chart_domain_many_2 = self.compute_same_domain_many(rec.ks_domain_many_2, rec.ks_domain_many_3, rec.ks_date_filter_field_many_2, ks_chart_groupby_relation_field_many, rec)

				orderby = rec.ks_sort_by_field_many.name if rec.ks_sort_by_field_many else "id"
				if rec.ks_sort_by_order:
					orderby = orderby + " " + rec.ks_sort_by_order
				limit = rec.ks_record_data_limit if rec.ks_record_data_limit and rec.ks_record_data_limit > 0 else False

				if rec.ks_chart_relation_groupby_many.ttype == 'date' and rec.ks_chart_date_groupby in ( 'minute', 'hour'):
					raise ValidationError(_('Groupby field: {} cannot be aggregated by {}').format(rec.ks_chart_relation_groupby.display_name, rec.ks_chart_date_groupby))
					ks_chart_date_groupby = 'day'
				else:
					ks_chart_date_groupby = rec.ks_chart_date_groupby


				if (rec.ks_chart_groupby_many_type == 'date_type' and rec.ks_chart_date_groupby) or rec.ks_chart_groupby_many_type != 'date_type':
					if rec.ks_chart_relation_groupby_many:
						if ((rec.ks_chart_measure_field_2_many and rec.ks_chart_measure_field_many) and \
								(rec.ks_chart_data_count_type_many_1  != 'count' and rec.ks_chart_data_count_type_many_2 != "count"))\
							or ((rec.ks_chart_measure_field_many and not rec.ks_chart_measure_field_2_many) and \
								(rec.ks_chart_data_count_type_many_1  != 'count' and rec.ks_chart_data_count_type_many_2 == "count"))\
							or((not rec.ks_chart_measure_field_many and rec.ks_chart_measure_field_2_many) and \
								(rec.ks_chart_data_count_type_many_1  == 'count' and rec.ks_chart_data_count_type_many_2 != "count"))\
							or((not rec.ks_chart_measure_field_many and not rec.ks_chart_measure_field_2_many) and \
								(rec.ks_chart_data_count_type_many_1  == 'count' and rec.ks_chart_data_count_type_many_2 == "count")) :

							data_1 = rec.ks_fetch_chart_data_many(
								rec.ks_model_name_many_1, ks_chart_domain_many_1,
								ks_chart_measure_field_many,
								ks_chart_groupby_relation_field_many,
								ks_chart_date_groupby,
								rec.ks_chart_groupby_many_type, orderby, limit,
								rec.ks_chart_data_count_type_many_1,
								rec.ks_chart_measure_field_many.ids,
								rec.ks_chart_relation_groupby_many.id,
								ks_chart_data_1
							)

							data_2 = rec.ks_fetch_chart_data_many(
								rec.ks_model_name_many_2, ks_chart_domain_many_2,
								ks_chart_measure_field_2_many,
								ks_chart_groupby_relation_field_many,
								ks_chart_date_groupby,
								rec.ks_chart_groupby_many_type, orderby, limit,
								rec.ks_chart_data_count_type_many_2,
								ks_chart_measure_field_2_ids_many,
								rec.ks_chart_relation_groupby_many.id,
								ks_chart_data_2
							)

							all_data_1 = get_all_data(data_1)
							all_data_2 = get_all_data(data_2)

							all_datasets = data_set_2 + data_set_1
							all_data = merge_all_data(all_data_1, all_data_2, data_1, data_2)
							final_data = create_data_structure(all_data, all_datasets)

							self.set_datasets_label_name(final_data)

							if rec.ks_unit and rec.ks_unit_selection == 'monetary':
								final_data['ks_selection'] += rec.ks_unit_selection
								final_data['ks_currency'] += rec.env.user.company_id.currency_id.id
							elif rec.ks_unit and rec.ks_unit_selection == 'custom':
								final_data['ks_selection'] += rec.ks_unit_selection
								if rec.ks_chart_unit:
									final_data['ks_field'] += rec.ks_chart_unit

							if rec.ks_monetary_unit_2_many:
								final_data['ks_monetary_unit_2_many'] += rec.env.user.company_id.currency_id.id

				rec.ks_chart_data = json.dumps(final_data)

			elif rec.ks_dashboard_item_type and rec.ks_dashboard_item_type != 'ks_tile' and rec.ks_dashboard_item_type != 'ks_bar_chart_many' and \
				rec.ks_dashboard_item_type != 'ks_list_view' and rec.ks_model_id and rec.ks_chart_data_count_type:

				ks_chart_data = {
					'labels': [], 
					'datasets': [], 
					'ks_currency': 0, 
					'ks_field': "", 
					'ks_selection': "", 
					'ks_show_second_y_scale': False, 
					'domains': [], 
				}

				ks_chart_measure_field = []
				ks_chart_measure_field_ids = []
				ks_chart_measure_field_2 = []
				ks_chart_measure_field_2_ids = []
				

				if rec.ks_unit and rec.ks_unit_selection == 'monetary':
					ks_chart_data['ks_selection'] += rec.ks_unit_selection
					ks_chart_data['ks_currency'] += rec.env.user.company_id.currency_id.id
				elif rec.ks_unit and rec.ks_unit_selection == 'custom':
					ks_chart_data['ks_selection'] += rec.ks_unit_selection
					if rec.ks_chart_unit:
						ks_chart_data['ks_field'] += rec.ks_chart_unit

				# If count chart data type:
				if rec.ks_chart_data_count_type == "count":
					ks_chart_data['datasets'].append({'data': [], 'label': "Count"})
				else:
					if rec.ks_dashboard_item_type == 'ks_bar_chart':
						if rec.ks_chart_measure_field_2:
							ks_chart_data['ks_show_second_y_scale'] = True

						for res in rec.ks_chart_measure_field_2:
							ks_chart_measure_field_2.append(res.name)
							ks_chart_measure_field_2_ids.append(res.id)
							ks_chart_data['datasets'].append(
								{'data': [], 'label': res.field_description, 'type': 'line', 'yAxisID': 'y-axis-1'})

					for res in rec.ks_chart_measure_field:
						ks_chart_measure_field.append(res.name)
						ks_chart_data['datasets'].append({'data': [], 'label': res.field_description})


				# ks_chart_measure_field = [res.name for res in rec.ks_chart_measure_field]
				ks_chart_groupby_relation_field = rec.ks_chart_relation_groupby.name

				ks_chart_domain = self.ks_convert_into_proper_domain(rec.ks_domain, rec)

				ks_chart_data['previous_domain'] = ks_chart_domain
				orderby = rec.ks_sort_by_field.name if rec.ks_sort_by_field else "id"
				if rec.ks_sort_by_order:
					orderby = orderby + " " + rec.ks_sort_by_order
				limit = rec.ks_record_data_limit if rec.ks_record_data_limit and rec.ks_record_data_limit > 0 else False

				if ((rec.ks_chart_data_count_type != "count" and ks_chart_measure_field) or (
						rec.ks_chart_data_count_type == "count" and not ks_chart_measure_field)) \
						and not rec.ks_chart_relation_sub_groupby:
					if rec.ks_chart_relation_groupby.ttype == 'date' and rec.ks_chart_date_groupby in (
							'minute', 'hour'):
						raise ValidationError(_('Groupby field: {} cannot be aggregated by {}').format(
							rec.ks_chart_relation_groupby.display_name, rec.ks_chart_date_groupby))
						ks_chart_date_groupby = 'day'
					else:
						ks_chart_date_groupby = rec.ks_chart_date_groupby

					if (rec.ks_chart_groupby_type == 'date_type' and rec.ks_chart_date_groupby) or rec.ks_chart_groupby_type != 'date_type':

						ks_chart_data = rec.ks_fetch_chart_data(rec.ks_model_name, ks_chart_domain,
																ks_chart_measure_field,
																ks_chart_measure_field_2,
																ks_chart_groupby_relation_field,
																ks_chart_date_groupby,
																rec.ks_chart_groupby_type, orderby, limit,
																rec.ks_chart_data_count_type,
																rec.ks_chart_measure_field.ids,
																ks_chart_measure_field_2_ids,
																rec.ks_chart_relation_groupby.id, ks_chart_data)

						if rec.ks_chart_groupby_type == 'date_type' and rec.ks_goal_enable and rec.ks_dashboard_item_type in ['ks_bar_chart', 'ks_horizontalBar_chart', 'ks_line_chart','ks_area_chart'] and rec.ks_chart_groupby_type == "date_type":

							if rec._context.get('current_id', False):
								ks_item_id = rec._context['current_id']
							else:
								ks_item_id = rec.id

							if rec.ks_date_filter_selection == "l_none":
								selected_start_date = rec._context.get('ksDateFilterStartDate', False)
								selected_end_date = rec._context.get('ksDateFilterEndDate', False)

							else:
								if rec.ks_date_filter_selection == "l_custom":
									selected_start_date  = rec.ks_item_start_date
									selected_end_date = rec.ks_item_start_date
								else:
									ks_date_data = ks_get_date(rec.ks_date_filter_selection)
									selected_start_date = ks_date_data["selected_start_date"]
									selected_end_date = ks_date_data["selected_end_date"]

							if selected_start_date and selected_end_date:
								selected_start_date = selected_start_date.strftime('%Y-%m-%d')
								selected_end_date = selected_end_date.strftime('%Y-%m-%d')
							ks_goal_domain = [('ks_dashboard_item', '=', ks_item_id)]

							if selected_start_date and selected_end_date:
								ks_goal_domain.extend([('ks_goal_date', '>=', selected_start_date.split(" ")[0]),
														('ks_goal_date', '<=', selected_end_date.split(" ")[0])])

							ks_date_data = rec.ks_get_start_end_date(rec.ks_model_name, ks_chart_groupby_relation_field,
																		rec.ks_chart_relation_groupby.ttype,
																		ks_chart_domain,
																		ks_goal_domain)

							labels = []
							if ks_date_data['start_date'] and ks_date_data['end_date'] and rec.ks_goal_lines:
								labels = self.generate_timeserise(ks_date_data['start_date'], ks_date_data['end_date'],
																	rec.ks_chart_date_groupby)

							ks_goal_records = self.env['ks_dashboard_ninja.item_goal'].read_group(
								ks_goal_domain, ['ks_goal_value'],
								['ks_goal_date' + ":" + ks_chart_date_groupby])
							ks_goal_labels = []
							ks_goal_dataset = []
							goal_dataset = []

							if rec.ks_goal_lines and len(rec.ks_goal_lines) != 0:
								ks_goal_domains = {}
								for res in ks_goal_records:
									if res['ks_goal_date' + ":" + ks_chart_date_groupby]:
										ks_goal_labels.append(res['ks_goal_date' + ":" + ks_chart_date_groupby])
										ks_goal_dataset.append(res['ks_goal_value'])
										ks_goal_domains[res['ks_goal_date' + ":" + ks_chart_date_groupby]] = res['__domain']

								for goal_domain in ks_goal_domains.keys():
									ks_goal_doamins = []
									for item in ks_goal_domains[goal_domain]:

										if 'ks_goal_date' in item:
											domain = list(item)
											domain[0] = ks_chart_groupby_relation_field
											domain = tuple(domain)
											ks_goal_doamins.append(domain)
									ks_goal_doamins.insert(0, '&')
									ks_goal_domains[goal_domain] = ks_goal_doamins

								domains = {}
								counter = 0
								for label in ks_chart_data['labels']:
									domains[label] = ks_chart_data['domains'][counter]
									counter += 1

								ks_chart_records_dates = ks_chart_data['labels'] + list(
									set(ks_goal_labels) - set(ks_chart_data['labels']))

								ks_chart_records = []
								for label in labels:
									if label in ks_chart_records_dates:
										ks_chart_records.append(label)

								ks_chart_data['domains'].clear()
								datasets = []
								for dataset in ks_chart_data['datasets']:
									datasets.append(dataset['data'].copy())

								for dataset in ks_chart_data['datasets']:
									dataset['data'].clear()

								for label in ks_chart_records:
									domain = domains.get(label, False)
									if domain:
										ks_chart_data['domains'].append(domain)
									else:
										ks_chart_data['domains'].append(ks_goal_domains.get(label, []))
									counterr = 0
									if label in ks_chart_data['labels']:
										index = ks_chart_data['labels'].index(label)

										for dataset in ks_chart_data['datasets']:
											dataset['data'].append(datasets[counterr][index])
											counterr += 1

									else:
										for dataset in ks_chart_data['datasets']:
											dataset['data'].append(0.00)

									if label in ks_goal_labels:
										index = ks_goal_labels.index(label)
										goal_dataset.append(ks_goal_dataset[index])
									else:
										goal_dataset.append(0.00)

								ks_chart_data['labels'] = ks_chart_records
							else:
								if rec.ks_standard_goal_value:
									length = len(ks_chart_data['datasets'][0]['data'])
									for i in range(length):
										goal_dataset.append(rec.ks_standard_goal_value)
							ks_goal_datasets = {
								'label': 'Target',
								'data': goal_dataset,
							}
							if rec.ks_goal_bar_line and rec.ks_dashboard_item_type == "ks_bar_chart":
								ks_goal_datasets['type'] = 'line'
								ks_chart_data['datasets'].insert(0, ks_goal_datasets)
							else:
								ks_chart_data['datasets'].append(ks_goal_datasets)

				elif rec.ks_chart_relation_sub_groupby and ((rec.ks_chart_sub_groupby_type == 'relational_type') or
															(rec.ks_chart_sub_groupby_type == 'selection') or
															(rec.ks_chart_sub_groupby_type == 'date_type' and
																rec.ks_chart_date_sub_groupby) or
															(rec.ks_chart_sub_groupby_type == 'other')):
					if rec.ks_chart_relation_sub_groupby.ttype == 'date':
						if rec.ks_chart_date_sub_groupby in ('minute', 'hour'):
							raise ValidationError(_('Sub Groupby field: {} cannot be aggregated by {}').format(
								rec.ks_chart_relation_sub_groupby.display_name, rec.ks_chart_date_sub_groupby))
						if rec.ks_chart_date_groupby in ('minute', 'hour'):
							raise ValidationError(_('Groupby field: {} cannot be aggregated by {}').format(
								rec.ks_chart_relation_sub_groupby.display_name, rec.ks_chart_date_groupby))
						# doesn't have time in date
						ks_chart_date_sub_groupby = rec.ks_chart_date_sub_groupby
						ks_chart_date_groupby = rec.ks_chart_date_groupby
					else:
						ks_chart_date_sub_groupby = rec.ks_chart_date_sub_groupby
						ks_chart_date_groupby = rec.ks_chart_date_groupby
					if len(ks_chart_measure_field) != 0 or rec.ks_chart_data_count_type == 'count':
						if rec.ks_chart_groupby_type == 'date_type' and ks_chart_date_groupby:
							ks_chart_group = rec.ks_chart_relation_groupby.name + ":" + ks_chart_date_groupby
						else:
							ks_chart_group = rec.ks_chart_relation_groupby.name

						if rec.ks_chart_sub_groupby_type == 'date_type' and rec.ks_chart_date_sub_groupby:
							ks_chart_sub_groupby_field = rec.ks_chart_relation_sub_groupby.name + ":" + \
															ks_chart_date_sub_groupby
						else:
							ks_chart_sub_groupby_field = rec.ks_chart_relation_sub_groupby.name

						ks_chart_groupby_relation_fields = [ks_chart_group, ks_chart_sub_groupby_field]
						ks_chart_record = self.env[rec.ks_model_name].read_group(ks_chart_domain,
																					set(ks_chart_measure_field +
																						ks_chart_measure_field_2 +
																						[ks_chart_groupby_relation_field,
																				rec.ks_chart_relation_sub_groupby.name]),
																					ks_chart_groupby_relation_fields,
																					orderby=orderby, limit=limit,
																					lazy=False)
						chart_data = []
						chart_sub_data = []
						for res in ks_chart_record:
							domain = res.get('__domain', [])
							if res[ks_chart_groupby_relation_fields[0]] and res[ks_chart_groupby_relation_fields[1]]:
								if rec.ks_chart_groupby_type == 'date_type':
									# x-axis modification
									if rec.ks_chart_date_groupby == "day" \
											and rec.ks_chart_date_sub_groupby in ["quarter", "year"]:
										label = " ".join(res[ks_chart_groupby_relation_fields[0]].split(" ")[:-1])
									elif rec.ks_chart_date_groupby == "day" \
											and rec.ks_chart_date_sub_groupby not in ["quarter", "year"]:
										label = res[ks_chart_groupby_relation_fields[0]].split(" ")[0]
									elif rec.ks_chart_date_groupby in ["minute", "hour"] and \
											rec.ks_chart_date_sub_groupby in ["month", "week", "quarter", "year"]:
										label = " ".join(res[ks_chart_groupby_relation_fields[0]].split(" ")[:])
									elif rec.ks_chart_date_groupby in ["minute", "hour"] and \
											rec.ks_chart_date_sub_groupby in ["minute", "hour", "day"]:
										label = res[ks_chart_groupby_relation_fields[0]].split(" ")[0]
									else:
										label = " ".join(res[ks_chart_groupby_relation_fields[0]].split(" ")[:-1])
								elif rec.ks_chart_groupby_type == 'selection':
									selection = res[ks_chart_groupby_relation_fields[0]]
									label = dict(self.env[rec.ks_model_name].fields_get(
										allfields=[ks_chart_groupby_relation_fields[0]])
													[ks_chart_groupby_relation_fields[0]]['selection'])[selection]
								elif rec.ks_chart_groupby_type == 'relational_type':
									label = res[ks_chart_groupby_relation_fields[0]][1]._value
								elif rec.ks_chart_groupby_type == 'other':
									label = res[ks_chart_groupby_relation_fields[0]]

								labels = []
								value = []
								value_2 = []
								labels_2 = []
								if rec.ks_chart_data_count_type != 'count':
									for ress in rec.ks_chart_measure_field:
										if rec.ks_chart_sub_groupby_type == 'date_type':
											labels.append(res[ks_chart_groupby_relation_fields[1]].split(" ")[
																0] + " " + ress.field_description)
										elif rec.ks_chart_sub_groupby_type == 'selection':
											selection = res[ks_chart_groupby_relation_fields[1]]
											labels.append(dict(self.env[rec.ks_model_name].fields_get(
												allfields=[ks_chart_groupby_relation_fields[1]])
																[ks_chart_groupby_relation_fields[1]]['selection'])[
																selection]
															+ " " + ress.field_description)
										elif rec.ks_chart_sub_groupby_type == 'relational_type':
											labels.append(res[ks_chart_groupby_relation_fields[1]][1]._value
															+ " " + ress.field_description)
										elif rec.ks_chart_sub_groupby_type == 'other':
											labels.append(str(res[ks_chart_groupby_relation_fields[1]])
															+ "\'s " + ress.field_description)

										value.append(res.get(
											ress.name) if rec.ks_chart_data_count_type == 'sum' else res.get(
											ress.name) / res.get('__count'))

									if rec.ks_chart_measure_field_2 and rec.ks_dashboard_item_type == 'ks_bar_chart':
										for ress in rec.ks_chart_measure_field_2:
											if rec.ks_chart_sub_groupby_type == 'date_type':
												labels_2.append(
													res[ks_chart_groupby_relation_fields[1]].split(" ")[0] + " "
													+ ress.field_description)
											elif rec.ks_chart_sub_groupby_type == 'selection':
												selection = res[ks_chart_groupby_relation_fields[1]]
												labels_2.append(dict(self.env[rec.ks_model_name].fields_get(
													allfields=[ks_chart_groupby_relation_fields[1]])
																		[ks_chart_groupby_relation_fields[1]][
																			'selection'])[
																	selection] + " " + ress.field_description)
											elif rec.ks_chart_sub_groupby_type == 'relational_type':
												labels_2.append(
													res[ks_chart_groupby_relation_fields[1]][1]._value + " " +
													ress.field_description)
											elif rec.ks_chart_sub_groupby_type == 'other':
												labels_2.append(str(
													res[ks_chart_groupby_relation_fields[1]]) + " " +
																ress.field_description)

											value_2.append(res.get(
												ress.name) if rec.ks_chart_data_count_type == 'sum' else res.get(
												ress.name) / res.get('__count'))

										chart_sub_data.append({
											'value': value_2,
											'labels': label,
											'series': labels_2,
											'domain': domain,
										})
								else:
									if rec.ks_chart_sub_groupby_type == 'date_type':
										labels.append(res[ks_chart_groupby_relation_fields[1]].split(" ")[0])
									elif rec.ks_chart_sub_groupby_type == 'selection':
										selection = res[ks_chart_groupby_relation_fields[1]]
										labels.append(dict(self.env[rec.ks_model_name].fields_get(
											allfields=[ks_chart_groupby_relation_fields[1]])
															[ks_chart_groupby_relation_fields[1]]['selection'])[
															selection])
									elif rec.ks_chart_sub_groupby_type == 'relational_type':
										labels.append(res[ks_chart_groupby_relation_fields[1]][1]._value)
									elif rec.ks_chart_sub_groupby_type == 'other':
										labels.append(res[ks_chart_groupby_relation_fields[1]])
									value.append(res['__count'])

								chart_data.append({
									'value': value,
									'labels': label,
									'series': labels,
									'domain': domain,
								})

						xlabels = []
						series = []
						values = {}
						domains = {}
						for data in chart_data:
							label = data['labels']
							serie = data['series']
							domain = data['domain']

							if (len(xlabels) == 0) or (label not in xlabels):
								xlabels.append(label)

							if (label not in domains):
								domains[label] = domain
							else:
								domains[label].insert(0, '|')
								domains[label] = domains[label] + domain

							series = series + serie
							value = data['value']
							counter = 0
							for seri in serie:
								if seri not in values:
									values[seri] = {}
								if label in values[seri]:
									values[seri][label] = values[seri][label] + value[counter]
								else:
									values[seri][label] = value[counter]
								counter += 1

						final_datasets = []
						for serie in series:
							if serie not in final_datasets:
								final_datasets.append(serie)

						ks_data = []
						for dataset in final_datasets:
							ks_dataset = {
								'value': [],
								'key': dataset
							}
							for label in xlabels:
								ks_dataset['value'].append({
									'domain': domains[label],
									'x': label,
									'y': values[dataset][label] if label in values[dataset] else 0
								})
							ks_data.append(ks_dataset)

						if rec.ks_chart_relation_sub_groupby.name == rec.ks_chart_relation_groupby.name == rec.ks_sort_by_field.name:
							ks_data = rec.ks_sort_sub_group_by_records(ks_data, rec.ks_chart_groupby_type,
																		rec.ks_chart_date_groupby, rec.ks_sort_by_order,
																		rec.ks_chart_date_sub_groupby)

						ks_chart_data = {
							'labels': [],
							'datasets': [],
							'domains': [],
							'ks_selection': "",
							'ks_currency': 0,
							'ks_field': "",
						}

						if rec.ks_unit and rec.ks_unit_selection == 'monetary':
							ks_chart_data['ks_selection'] += rec.ks_unit_selection
							ks_chart_data['ks_currency'] += rec.env.user.company_id.currency_id.id
						elif rec.ks_unit and rec.ks_unit_selection == 'custom':
							ks_chart_data['ks_selection'] += rec.ks_unit_selection
							if rec.ks_chart_unit:
								ks_chart_data['ks_field'] += rec.ks_chart_unit

						if len(ks_data) != 0:
							for res in ks_data[0]['value']:
								ks_chart_data['labels'].append(res['x'])
								ks_chart_data['domains'].append(res['domain'])
							if rec.ks_chart_measure_field_2 and rec.ks_dashboard_item_type == 'ks_bar_chart':
								ks_chart_data['ks_show_second_y_scale'] = True
								values_2 = {}
								series_2 = []
								for data in chart_sub_data:
									label = data['labels']
									serie = data['series']
									series_2 = series_2 + serie
									value = data['value']

									counter = 0
									for seri in serie:
										if seri not in values_2:
											values_2[seri] = {}
										if label in values_2[seri]:
											values_2[seri][label] = values_2[seri][label] + value[counter]
										else:
											values_2[seri][label] = value[counter]
										counter += 1
								final_datasets_2 = []
								for serie in series_2:
									if serie not in final_datasets_2:
										final_datasets_2.append(serie)
								ks_data_2 = []
								for dataset in final_datasets_2:
									ks_dataset = {
										'value': [],
										'key': dataset
									}
									for label in xlabels:
										ks_dataset['value'].append({
											'x': label,
											'y': values_2[dataset][label] if label in values_2[dataset] else 0
										})
									ks_data_2.append(ks_dataset)

								for ks_dat in ks_data_2:
									dataset = {
										'label': ks_dat['key'],
										'data': [],
										'type': 'line',
										'yAxisID': 'y-axis-1'

									}
									for res in ks_dat['value']:
										dataset['data'].append(res['y'])

									ks_chart_data['datasets'].append(dataset)
							for ks_dat in ks_data:
								dataset = {
									'label': ks_dat['key'],
									'data': []
								}
								for res in ks_dat['value']:
									dataset['data'].append(res['y'])

								ks_chart_data['datasets'].append(dataset)

							if rec.ks_goal_enable and rec.ks_standard_goal_value and rec.ks_dashboard_item_type in [
								'ks_bar_chart', 'ks_line_chart', 'ks_area_chart', 'ks_horizontalBar_chart']:
								goal_dataset = []
								length = len(ks_chart_data['datasets'][0]['data'])
								for i in range(length):
									goal_dataset.append(rec.ks_standard_goal_value)
								ks_goal_datasets = {
									'label': 'Target',
									'data': goal_dataset,
								}
								if rec.ks_goal_bar_line and rec.ks_dashboard_item_type != 'ks_horizontalBar_chart':
									ks_goal_datasets['type'] = 'line'
									ks_chart_data['datasets'].insert(0, ks_goal_datasets)
								else:
									ks_chart_data['datasets'].append(ks_goal_datasets)
					else:
						ks_chart_data = False
				
				self.set_datasets_label_name(ks_chart_data)
				
				rec.ks_chart_data = json.dumps(ks_chart_data)

			else:
				rec.ks_chart_data = False

	def set_datasets_label_name(self, final_data):
		for rec in self:
			datasets_field_1_line = [
				rec.ks_chart_measure_field_name_1_1,
				rec.ks_chart_measure_field_name_1_2,
				rec.ks_chart_measure_field_name_1_3,
				rec.ks_chart_measure_field_name_1_4
			]

			datasets_field_2_bar = [
				rec.ks_chart_measure_field_name_2_1,
				rec.ks_chart_measure_field_name_2_2,
				rec.ks_chart_measure_field_name_2_3,
				rec.ks_chart_measure_field_name_2_4
			]

			if rec.ks_dashboard_item_type == 'ks_bar_chart_many' or rec.ks_dashboard_item_type == 'ks_bar_chart':
				counter = 0
				for data in final_data['datasets']:
					if len(data) > 2:
						data['label'] = datasets_field_2_bar[counter]
						counter += 1
					else:
						break

				counter_data_1 = 0
				for x in range(counter, len(final_data['datasets'])):
					final_data['datasets'][x]['label'] = datasets_field_1_line[counter_data_1]
					counter_data_1 += 1
			else:
				if len(final_data['datasets']) > 4:
					raise ValidationError(f'You can only select up to 4 values.')
				else:
					counter = 0
					for data in final_data['datasets']:
						data['label'] = datasets_field_1_line[counter]
						counter += 1

			print()

	def ks_fetch_chart_data_many(self, ks_model_name, ks_chart_domain, ks_chart_measure_field, 
							ks_chart_groupby_relation_field, ks_chart_date_groupby, ks_chart_groupby_type, orderby,
							limit, chart_count, ks_chart_measure_field_ids,
							ks_chart_groupby_relation_field_id, ks_chart_data):
		if ks_chart_groupby_type == "date_type":
			ks_chart_groupby_field = ks_chart_groupby_relation_field + ":" + ks_chart_date_groupby
		else:
			ks_chart_groupby_field = ks_chart_groupby_relation_field
		try:
			ks_chart_records = self.env[ks_model_name].read_group(ks_chart_domain, 
																set( ks_chart_measure_field + [ks_chart_groupby_relation_field]),
																[ks_chart_groupby_field],
																orderby=orderby, 
																limit=limit)

		except Exception as e:
			ks_chart_records = []
			pass

		ks_chart_data['groupby'] = ks_chart_groupby_field
		if ks_chart_groupby_type == "relational_type":
			ks_chart_data['groupByIds'] = []

		for res in ks_chart_records:
			if all(measure_field in res for measure_field in ks_chart_measure_field):
				if ks_chart_groupby_type == "relational_type":
					if res[ks_chart_groupby_field]:
						ks_chart_data['labels'].append(res[ks_chart_groupby_field][1]._value)
						ks_chart_data['groupByIds'].append(res[ks_chart_groupby_field][0])
					else:
						ks_chart_data['labels'].append(res[ks_chart_groupby_field])
				elif ks_chart_groupby_type == "selection":
					selection = res[ks_chart_groupby_field]
					if selection:
						ks_chart_data['labels'].append(
							dict(self.env[ks_model_name].fields_get(allfields=[ks_chart_groupby_field])
								[ks_chart_groupby_field]['selection'])[selection])
					else:
						ks_chart_data['labels'].append(selection)
				else:
					ks_chart_data['labels'].append(res[ks_chart_groupby_field])

				ks_chart_data['domains'].append(res.get('__domain', []))
				counter = 0
				if ks_chart_measure_field:
					index = 0
					for field_rec in ks_chart_measure_field:
						ks_groupby_equal_measures = res[ks_chart_groupby_relation_field + "_count"] \
							if ks_chart_measure_field_ids[index] == ks_chart_groupby_relation_field_id \
							else 1
						data = res[field_rec] * ks_groupby_equal_measures \
							if chart_count == 'sum' \
							else res[field_rec] * ks_groupby_equal_measures / res[ks_chart_groupby_relation_field + "_count"]
						ks_chart_data['datasets'][counter]['data'].append(data)
						counter += 1
					index += 1
				else:
					data = res[ks_chart_groupby_relation_field + "_count"]
					ks_chart_data['datasets'][0]['data'].append(data)

		return ks_chart_data

	def compute_same_domain_many(self, domain, common_domain, date_filter_field, groupby_relation_field_many, rec):

		common_domain = ast.literal_eval(common_domain) if isinstance(common_domain, str) else []
		domain = ast.literal_eval(domain) if isinstance(domain, str) else []

		same_domain = [x for x in common_domain if x[0] == groupby_relation_field_many]
		len_same_domain = len(same_domain)

		domain.extend([[groupby_relation_field_many, '!=', False]])
		domain.extend(['|'] * (len_same_domain - 1))
		domain.extend(same_domain)

		ks_chart_domain = self.ks_convert_into_proper_domain_many(str(domain), date_filter_field, rec)

		return ks_chart_domain

	def ks_convert_into_proper_domain_many(self, ks_domain, ks_date_filter_field_many,  rec):
		if ks_domain and "%UID" in ks_domain:
			ks_domain = ks_domain.replace('"%UID"', str(self.env.user.id))
			print(ks_domain)

		if ks_domain and "%MYCOMPANY" in ks_domain:
			ks_domain = ks_domain.replace('"%MYCOMPANY"', str(self.env.user.company_id.id))
			print(ks_domain)
		ks_date_domain = False

		if not rec.ks_date_filter_selection or rec.ks_date_filter_selection == "l_none":
			selected_start_date = self._context.get('ksDateFilterStartDate', False)
			selected_end_date = self._context.get('ksDateFilterEndDate', False)
			if selected_start_date and selected_end_date and ks_date_filter_field_many.name:
				ks_date_domain = [
					(ks_date_filter_field_many.name, ">=", selected_start_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)),
					(ks_date_filter_field_many.name, "<=", selected_end_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT))
				]
		else:
			if rec.ks_date_filter_selection and rec.ks_date_filter_selection != 'l_custom':
				ks_date_data = ks_get_date(rec.ks_date_filter_selection)
				selected_start_date = ks_date_data["selected_start_date"]
				selected_end_date = ks_date_data["selected_end_date"]
			else:
				if rec.ks_item_start_date or rec.ks_item_end_date:
					selected_start_date = rec.ks_item_start_date
					selected_end_date = rec.ks_item_end_date

			if selected_start_date and selected_end_date:
				if rec.ks_compare_period:
					ks_compare_period = abs(rec.ks_compare_period)
					if ks_compare_period > 100:
						ks_compare_period = 100
					if rec.ks_compare_period > 0:
						selected_end_date = selected_end_date + (selected_end_date - selected_start_date) * ks_compare_period
					elif rec.ks_compare_period < 0:
						selected_start_date = selected_start_date - (selected_end_date - selected_start_date) * ks_compare_period

				if rec.ks_year_period and rec.ks_year_period != 0 and rec.ks_dashboard_item_type:
					abs_year_period = abs(rec.ks_year_period)
					sign_yp = rec.ks_year_period / abs_year_period
					if abs_year_period > 10:
						abs_year_period = 10
					date_field_name = ks_date_filter_field_many.name

					ks_date_domain = [
						'&',
						(date_field_name, ">=", fields.datetime.strftime(selected_start_date, DEFAULT_SERVER_DATETIME_FORMAT)),
						(date_field_name, "<=", fields.datetime.strftime(selected_end_date, DEFAULT_SERVER_DATETIME_FORMAT))
					]

					for p in range(1, abs_year_period + 1):
						ks_date_domain.insert(0, '|')
						ks_date_domain.extend([
							'&',
							(date_field_name, ">=", fields.datetime.strftime( selected_start_date - relativedelta.relativedelta(years=p) * sign_yp, DEFAULT_SERVER_DATETIME_FORMAT)),
							(date_field_name, "<=", fields.datetime.strftime(selected_end_date - relativedelta.relativedelta(years=p) * sign_yp, DEFAULT_SERVER_DATETIME_FORMAT))
						])
				else:
					if ks_date_filter_field_many:
						selected_start_date = fields.datetime.strftime(selected_start_date, DEFAULT_SERVER_DATETIME_FORMAT)
						selected_end_date = fields.datetime.strftime(selected_end_date, DEFAULT_SERVER_DATETIME_FORMAT)
						ks_date_domain = [(ks_date_filter_field_many.name, ">=", selected_start_date), (ks_date_filter_field_many.name, "<=", selected_end_date)]
					else:
						ks_date_domain = []

		proper_domain = eval(ks_domain) if ks_domain else []
		
		if ks_date_domain:
			proper_domain.extend(ks_date_domain)

		return proper_domain


def get_all_data(raw_data):
	all_data = []

	for x in range(len(raw_data['groupByIds'])):
		datasets = []
		for data in raw_data['datasets']:
			datasets.append(data['data'][x])

		all_data.append([
			raw_data['groupByIds'][x],
			raw_data['labels'][x],
			raw_data['domains'][x],
			datasets
		])

	return all_data

def	merge_all_data(all_data_1, all_data_2, data_1, data_2):
	data_1_null = []
	for x in range(len(data_1['labels']) - 1):
		data_1_null.append(0.0)

	data_2_null = []
	for x in range(len(data_2['labels']) - 1):
		data_2_null.append(0.0)

	all_data_id_1 = []
	all_data_id_2 = []
	for data in all_data_1:
		all_data_id_1.append(data[0])
	for data in all_data_2:
		all_data_id_2.append(data[0])

	all_data = sorted(set(all_data_id_1).union(all_data_id_2))
	len_ids = len(all_data)

	for x in range(len_ids):
		for data in all_data_1:
			if data[0] == all_data[x]:
				all_data[x] = data

	for x in range(len_ids):
		for data in all_data_2:
			if isinstance(all_data[x], int) and (data[0] == all_data[x]) :
				all_data[x] = [data[0],data[1],data[2],data_1_null,data[3]]

			elif (isinstance(all_data[x], list)) and (data[0] == all_data[x][0]):
				all_data[x].append(data[3])

	for x in range(len_ids):
		if len(all_data[x]) == 4:
			all_data[x].append(data_2_null)

	return all_data

def create_data_structure(data_list, label_measure_fields):
	ks_chart_data = {
		"labels": [],
		"domains": [],
		"groupByIds": [],
		"datasets": [

		],
		"groupby": "",
		# "ks_monetary_unit_1_many": 0,
		"ks_monetary_unit_2_many": 0,
		"ks_monetary_unit": 0,
		"ks_selection": "", 
		"ks_currency" : 0,
		"ks_field": "",
		"ks_show_second_y_scale": True,
		"previous_domain": [],
	}

	for x in label_measure_fields:
		ks_chart_data['datasets'].append(x)

	for data in data_list:
		id_label = data[0]
		label = data[1]
		domains = data[2]
		datasets_1 = data[4]
		datasets_2 = data[3]

		if isinstance(label, str):
			ks_chart_data['labels'].append(label)
		else : 
			ks_chart_data['labels'].append(str(label))

		ks_chart_data['domains'].append(domains)
		ks_chart_data['groupByIds'].append(id_label)

		all_data_value = []

		for index in range(len(datasets_1)):
			all_data_value.append(datasets_1[index])

		for index in range(len(datasets_2)):
			all_data_value.append(datasets_2[index])

		for dataset, value in zip(ks_chart_data['datasets'], all_data_value):
			dataset['data'].append(value)

	return ks_chart_data

def print_all(x):
	print()
	print()
	print(str(x))
	for y in x:
		print(y)
	print()
	print()

def print_one(x,name=''):
	print()
	print(name)
	print(x)
	print()


#  add ks_show_gridlines field to these item 
class KsDashboardNinjaBoard(models.Model):
	_inherit = "ks_dashboard_ninja.board"
	# fetching Item info (Divided to make function inherit easily)


	# @api.model
	# def default_get(self, fields):
	# 	res = super(KsDashboardNinjaBoard, self).default_get(fields)
	# 	if 'ks_dashboard_top_menu_id' in fields:  # avoid forcing the partner of the first lead as default
	# 		menu_root = self.env.ref('ks_dashboard_ninja.dashboards_menu_list', raise_if_not_found=False)
	# 		if bool(menu_root):
	# 			res['ks_dashboard_top_menu_id'] = self.env.ref('ks_dashboard_ninja.dashboards_menu_list', raise_if_not_found=False).id
	# 	return res


	def ks_fetch_item_data(self, rec):
		"""
		:rtype: object
		:param item_id: item object
		:return: object with formatted item data
		"""
		if rec.ks_actions:
			action = {}
			action['name'] = rec.ks_actions.name
			action['type'] = rec.ks_actions.type
			action['res_model'] = rec.ks_actions.res_model
			action['views'] = rec.ks_actions.views
			action['view_mode'] = rec.ks_actions.view_mode
			action['target'] = 'current'
		else:
			action = False
		item = {
			'name': rec.name if rec.name else rec.ks_model_id.name if rec.ks_model_id else "",
			'ks_background_color': rec.ks_background_color,
			'ks_font_color': rec.ks_font_color,
			'ks_zoom': rec.ks_zoom,
			# 'ks_domain': rec.ks_domain.replace('"%UID"', str(
			#     self.env.user.id)) if rec.ks_domain and "%UID" in rec.ks_domain else rec.ks_domain,
			'ks_domain': rec.ks_convert_into_proper_domain(rec.ks_domain, rec),
			'ks_dashboard_id': rec.ks_dashboard_ninja_board_id.id,
			'ks_icon': rec.ks_icon,
			'ks_model_id': rec.ks_model_id.id,
			'ks_model_name': rec.ks_model_name,
			'ks_model_display_name': rec.ks_model_id.name,
			'ks_record_count_type': rec.ks_record_count_type,
			'ks_record_count': rec.ks_record_count,
			'id': rec.id,
			'ks_layout': rec.ks_layout,
			'ks_icon_select': rec.ks_icon_select,
			'ks_default_icon': rec.ks_default_icon,
			'ks_default_icon_color': rec.ks_default_icon_color,
			# Pro Fields
			'ks_dashboard_item_type': rec.ks_dashboard_item_type,
			'ks_chart_item_color': rec.ks_chart_item_color,
			'ks_chart_groupby_type': rec.ks_chart_groupby_type,
			'ks_chart_relation_groupby': rec.ks_chart_relation_groupby.id,
			'ks_chart_relation_groupby_name': rec.ks_chart_relation_groupby.name,
			'ks_chart_date_groupby': rec.ks_chart_date_groupby,
			'ks_record_field': rec.ks_record_field.id if rec.ks_record_field else False,
			'ks_chart_data': rec.ks_chart_data,
			'ks_list_view_data': rec.ks_list_view_data,
			'ks_chart_data_count_type': rec.ks_chart_data_count_type,
			'ks_bar_chart_stacked': rec.ks_bar_chart_stacked,
			'ks_semi_circle_chart': rec.ks_semi_circle_chart,
			'ks_list_view_type': rec.ks_list_view_type,
			'ks_list_view_group_fields': rec.ks_list_view_group_fields.ids if rec.ks_list_view_group_fields else False,
			'ks_previous_period': rec.ks_previous_period,
			'ks_kpi_data': rec.ks_kpi_data,
			'ks_goal_enable': rec.ks_goal_enable,
			'ks_model_id_2': rec.ks_model_id_2.id,
			'ks_record_field_2': rec.ks_record_field_2.id,
			'ks_data_comparison': rec.ks_data_comparison,
			'ks_target_view': rec.ks_target_view,
			'ks_date_filter_selection': rec.ks_date_filter_selection,
			'ks_show_data_value': rec.ks_show_data_value,
			'ks_show_gridlines': rec.ks_show_gridlines,
			'ks_chart_x_axe_font_size': rec.ks_chart_x_axe_font_size,
			'ks_chart_y_axe_font_size': rec.ks_chart_y_axe_font_size,
			'ks_chart_legend_font_size': rec.ks_chart_legend_font_size,
			'ks_chart_title_font_size': rec.ks_chart_title_font_size,
			'ks_update_items_data': rec.ks_update_items_data,
			'ks_show_records': rec.ks_show_records,
 			'sequence': 0,
			'max_sequnce': len(rec.ks_action_lines) if rec.ks_action_lines else False,
			'action': action
		}
		return item

	def ks_export_item_data(self, rec):
		ks_chart_measure_field = []
		ks_chart_measure_field_2 = []
		for res in rec.ks_chart_measure_field:
			ks_chart_measure_field.append(res.name)
		for res in rec.ks_chart_measure_field_2:
			ks_chart_measure_field_2.append(res.name)

		ks_list_view_group_fields = []
		for res in rec.ks_list_view_group_fields:
			ks_list_view_group_fields.append(res.name)

		ks_goal_lines = []
		for res in rec.ks_goal_lines:
			goal_line = {
				'ks_goal_date': datetime.datetime.strftime(res.ks_goal_date, "%Y-%m-%d"),
				'ks_goal_value': res.ks_goal_value,
			}
			ks_goal_lines.append(goal_line)

		ks_action_lines = []
		for res in rec.ks_action_lines:
			action_line = {
				'ks_item_action_field': res.ks_item_action_field.name,
				'ks_item_action_date_groupby': res.ks_item_action_date_groupby,
				'ks_chart_type': res.ks_chart_type,
				'ks_sort_by_field': res.ks_sort_by_field.name,
				'ks_sort_by_order': res.ks_sort_by_order,
				'ks_record_limit': res.ks_record_limit,
				'sequence': res.sequence,
			}
			ks_action_lines.append(action_line)

		ks_list_view_field = []
		for res in rec.ks_list_view_fields:
			ks_list_view_field.append(res.name)
		item = {
			'name': rec.name if rec.name else rec.ks_model_id.name if rec.ks_model_id else "Name",
			'ks_background_color': rec.ks_background_color,
			'ks_font_color': rec.ks_font_color,
			'ks_domain': rec.ks_domain,
			'ks_icon': rec.ks_icon,
			'ks_id': rec.id,
			'ks_model_id': rec.ks_model_name,
			'ks_record_count': rec.ks_record_count,
			'ks_layout': rec.ks_layout,
			'ks_icon_select': rec.ks_icon_select,
			'ks_default_icon': rec.ks_default_icon,
			'ks_default_icon_color': rec.ks_default_icon_color,
			'ks_record_count_type': rec.ks_record_count_type,
			# Pro Fields
			'ks_dashboard_item_type': rec.ks_dashboard_item_type,
			'ks_chart_item_color': rec.ks_chart_item_color,
			'ks_chart_groupby_type': rec.ks_chart_groupby_type,
			'ks_chart_relation_groupby': rec.ks_chart_relation_groupby.name,
			'ks_chart_date_groupby': rec.ks_chart_date_groupby,
			'ks_record_field': rec.ks_record_field.name,
			'ks_chart_sub_groupby_type': rec.ks_chart_sub_groupby_type,
			'ks_chart_relation_sub_groupby': rec.ks_chart_relation_sub_groupby.name,
			'ks_chart_date_sub_groupby': rec.ks_chart_date_sub_groupby,
			'ks_chart_data_count_type': rec.ks_chart_data_count_type,
			'ks_chart_measure_field': ks_chart_measure_field,
			'ks_chart_measure_field_2': ks_chart_measure_field_2,
			'ks_list_view_fields': ks_list_view_field,
			'ks_list_view_group_fields': ks_list_view_group_fields,
			'ks_list_view_type': rec.ks_list_view_type,
			'ks_record_data_limit': rec.ks_record_data_limit,
			'ks_sort_by_order': rec.ks_sort_by_order,
			'ks_sort_by_field': rec.ks_sort_by_field.name,
			'ks_date_filter_field': rec.ks_date_filter_field.name,
			'ks_goal_enable': rec.ks_goal_enable,
			'ks_standard_goal_value': rec.ks_standard_goal_value,
			'ks_goal_liness': ks_goal_lines,
			'ks_date_filter_selection': rec.ks_date_filter_selection,
			'ks_item_start_date':rec.ks_item_start_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT) if rec.ks_item_start_date else False,
			'ks_item_end_date': rec.ks_item_end_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT) if rec.ks_item_end_date else False,
			'ks_date_filter_selection_2': rec.ks_date_filter_selection_2,
			'ks_item_start_date_2': rec.ks_item_start_date_2.strftime(DEFAULT_SERVER_DATETIME_FORMAT) if rec.ks_item_start_date_2 else False,
			'ks_item_end_date_2': rec.ks_item_end_date_2.strftime(DEFAULT_SERVER_DATETIME_FORMAT) if rec.ks_item_end_date_2 else False,
			'ks_previous_period': rec.ks_previous_period,
			'ks_target_view': rec.ks_target_view,
			'ks_data_comparison': rec.ks_data_comparison,
			'ks_record_count_type_2': rec.ks_record_count_type_2,
			'ks_record_field_2': rec.ks_record_field_2.name,
			'ks_model_id_2': rec.ks_model_id_2.model,
			'ks_date_filter_field_2': rec.ks_date_filter_field_2.name,
			'ks_action_liness': ks_action_lines,
			'ks_compare_period': rec.ks_compare_period,
			'ks_year_period': rec.ks_year_period,
			'ks_compare_period_2': rec.ks_compare_period_2,
			'ks_year_period_2': rec.ks_year_period_2,
			'ks_domain_2': rec.ks_domain_2,
			'ks_show_data_value': rec.ks_show_data_value,
			'ks_show_gridlines': rec.ks_show_gridlines,
			'ks_chart_x_axe_font_size': rec.ks_chart_x_axe_font_size,
			'ks_chart_y_axe_font_size': rec.ks_chart_y_axe_font_size,
			'ks_chart_legend_font_size': rec.ks_chart_legend_font_size,
			'ks_chart_title_font_size': rec.ks_chart_title_font_size,
			'ks_update_items_data': rec.ks_update_items_data,
			'ks_list_target_deviation_field': rec.ks_list_target_deviation_field.name,
			'ks_unit': rec.ks_unit,
			'ks_show_records': rec.ks_show_records,
			'ks_chart_unit': rec.ks_chart_unit,
			'ks_unit_selection': rec.ks_unit_selection,
			# 'ks_monetary_unit_1_many': rec.ks_monetary_unit_1_many,
			'ks_monetary_unit_2_many': rec.ks_monetary_unit_2_many,
			'ks_bar_chart_stacked': rec.ks_bar_chart_stacked,
			'ks_goal_bar_line': rec.ks_goal_bar_line,
			'ks_actions': rec.ks_actions.xml_id if rec.ks_actions else False
		}
		return item







