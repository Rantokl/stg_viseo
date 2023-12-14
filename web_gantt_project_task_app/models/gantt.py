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
	next_project = fields.Many2one('viseo.project.project', string='Projet suivant')

	# def _compute_next_project(self):
	# 	return 


	# @api.onchange('next_project')
	# def _onchange_next_project(self):
	# 	# Update the hierarchical order based on the selected next project
	# 	if self.next_project:
	# 		self._swap_projects(self, self.next_project)

	# def _swap_projects(self, project1, project2):
	# 	# Swap the parent_id values of the two projects
	# 	project1_parent = project1.parent_id
	# 	project2_parent = project2.parent_id

	# 	project1.write({'parent_id': project2_parent.id})
	# 	project2.write({'parent_id': project1_parent.id})


	@api.depends('parent_id', 'parent_id.hierarchical_id')
	def _compute_hierarchical_id(self):
		for project in self:
			hierarchical_id = ''

			# If the project has a parent, get the parent's hierarchical ID and count the number of siblings
			if project.parent_id:
				parent_hierarchical_id = project.parent_id.hierarchical_id
				sibling_count = self.search_count([('parent_id', '=', project.parent_id.id), ('id', '<=', project.id)])
				hierarchical_id = f'{parent_hierarchical_id}-{sibling_count}'

			# If the project has no parent, it's a root project, so use its own creation sequence
			else:
				root_count = self.search_count([('parent_id', '=', False), ('id', '<=', project.id)])
				hierarchical_id = f'{root_count}'

			project.hierarchical_id = hierarchical_id


			next_sibling = self.search([
				('parent_id', '=', project.parent_id.id),
				('hierarchical_id', '=', int(project.hierarchical_id[-1] - 1))
			], limit=1)
			if next_sibling:
				project.next_project = next_sibling.id
			else:
				project.next_project = False



	hierarchical_id = fields.Char(
		string='Hierarchical ID',
		compute='_compute_hierarchical_id'
	)


	def get_ganttt_data(self, project_id=None):
		record_id = int(self.id)
		
		project_ids = self.env['viseo.project.project'].browse([record_id])

		def create_data_structure(project, hierarchical_parent_Id):
			
			hierarchical_parent_Id = int_To_Roman(hierarchical_parent_Id) if isinstance(hierarchical_parent_Id, int) else hierarchical_parent_Id

			data = {
				'type': 'project',
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
					'type': 'task',
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

	# hierarchical_id = fields.Char(
	# 	string='Hierarchical ID',
	# 	default='_compute_hierarchical_id',
	# 	store=True,  # Set store to True if you want to store the computed value in the database
	# )

	# @api.depends('parent_id', 'parent_id.hierarchical_id')
	# def _compute_hierarchical_id(self):
	# 	for project in self:
	# 		hierarchical_id = str(project.id)
	# 		parent = project.parent_id

	# 		while parent:
	# 			hierarchical_id = str(parent.id) + '-' + hierarchical_id
	# 			parent = parent.parent_id

	# 		project.hierarchical_id = hierarchical_id









