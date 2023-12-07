# -*- coding: utf-8 -*-

from odoo import models, fields, models, api
from datetime import datetime
from pprint import pprint
import socket

class GanttView(models.Model):
	_inherit = 'viseo.project.project'
	start_date = fields.Date(string="Date debut")
	end_date = fields.Date(string="Date fin")

	project_description = fields.Html(string='Description')	

	def get_ganttt_data(self, project_id=None):
		record_id = int(self.id)
		print()
		print()
		print(record_id)
		print()
		print()

		project_ids = self.env['viseo.project.project'].browse([record_id])

		print()
		print()
		print(project_ids)
		print()
		print()

		def create_data_structure(project, hierarchical_parent_Id):
			
			hierarchical_parent_Id = int_To_Roman(hierarchical_parent_Id) if isinstance(hierarchical_parent_Id, int) else hierarchical_parent_Id

			data = {
				'redirection_Id': project.id,
				'id': hierarchical_parent_Id,
				'name': project.name,
				'actualStart': None,
				'actualEnd': None,
				'children': []
			}

			task_id_Counter = 1

			for task in project.task_ids:
				actual_start = ''
				actual_end = ''
				hierarchical_Id = f"{hierarchical_parent_Id}-{convert_int_to_char(task_id_Counter)}"

				if task.date_start and task.date_deadline:
					actual_start = task.date_start.strftime("%Y-%m-%d")
					child_date_deadline = datetime.strptime(task.date_deadline.strftime("%Y-%m-%d"),  "%Y-%m-%d").date()
					actual_end = child_date_deadline.strftime("%Y-%m-%d")
				else: 
					actual_start = None
					actual_end = None

				data['children'].append({
					'redirection_Id': task.id,
					'id': hierarchical_Id,
					'name': task.name,
					'actualStart': actual_start,
					'actualEnd': actual_end
				})

				task_id_Counter += 1

			if project.child_ids:
				for sub_project in project.child_ids:
					hierarchical_Id = f"{hierarchical_parent_Id}-{task_id_Counter}"
					sub_project_data = create_data_structure(sub_project, hierarchical_Id)
					data['children'].append(sub_project_data)
					task_id_Counter += 1

			data['actualStart'] = project.start_date if project.start_date else actual_start if 'actual_start' in locals() else None
			data['actualEnd'] = project.end_date if project.end_date else actual_end if 'actual_end' in locals() else None

			return data

		all_projects = [create_data_structure(project_ids, 1)]

		print()
		for x in all_projects:
			pprint(x, sort_dicts=False)
		print()

		return all_projects

		return []

def convert_int_to_char(id_counter):
	alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	return alphabet[id_counter - 1]


def int_To_Roman(num):
	m = ["", "M", "MM", "MMM"]
	c = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM "]
	x = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
	i = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

	thousands = m[num // 1000]
	hundreds = c[(num % 1000) // 100]
	tens = x[(num % 100) // 10]
	ones = i[num % 10]
	ans = (thousands + hundreds + tens + ones)
 
	return ans

class ViseoTask(models.Model):
	_inherit = "viseo.project.task"

	date_start = fields.Date(string='Start', index=True, copy=False, tracking=True)



