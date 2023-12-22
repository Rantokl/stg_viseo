# -*- coding: utf-8 -*-

from odoo import models, fields, models, api
from datetime import datetime
from pprint import pprint
import socket

class GanttView(models.Model):
	_inherit = 'viseo.project.project'
	_order = 'hierarchical_id'
	start_date = fields.Date(string="Date debut")
	end_date = fields.Date(string="Date fin")

	project_description = fields.Html(string='Description')
	precedent_project_id = fields.Many2one('viseo.project.project', string='Projet prédédent', domain="[('parent_id', '=', parent_id)]")
	hierarchical_id = fields.Char( string='Hierarchical ID')

	@api.onchange('precedent_project_id')
	def _onchange_precedent_project(self):
		if self.precedent_project_id:
			# Get the sibling projects
			sibling = self.env['viseo.project.project'].search([('parent_id', '=', False)])
			sorted_hierarchical_ids = self.get_projects(sibling)
			precedent_sub_id = self.get_sub_id(self.precedent_project_id.hierarchical_id)
			precedent_index = sorted_hierarchical_ids.index(self.precedent_project_id.hierarchical_id)
			max_hierarchical_id = len(sorted_hierarchical_ids) + 1
			self.hierarchical_id = f'{precedent_sub_id + 1}'
			current_index = sorted_hierarchical_ids.index(self.hierarchical_id)
			for i in range(current_index + 1, len(sorted_hierarchical_ids)):
				sub_id = self.get_sub_id(sorted_hierarchical_ids[i - 1]) + 1
				if sub_id > max_hierarchical_id:
					sub_id = max_hierarchical_id
				sorted_hierarchical_ids[i] = f'{sub_id}'
			self.hierarchical_id = f'{precedent_sub_id + 1}'


	def get_projects(self, sibling):
		all_siblings = []
		for sib in sibling:
			all_siblings.append(sib.hierarchical_id)
		
		return sorted(all_siblings)


	def get_sub_id(self, id):
		return int(id.split('-')[-1])


	@api.model
	def create(self, vals):
		if vals.get('parent_id'):
			parent = self.env['viseo.project.project'].browse(vals['parent_id'])
			siblings = self.env['viseo.project.project'].search([('parent_id', '=', vals['parent_id'])])
			sibling_count = len(siblings)
			hierarchical_id = f'{parent.hierarchical_id}-{sibling_count + 1}'
		else:
			siblings = self.env['viseo.project.project'].search([('parent_id', '=', False)])
			root_count = len(siblings)
			hierarchical_id = f'{root_count + 1}'

		vals['hierarchical_id'] = hierarchical_id

		sub_id = int(hierarchical_id.split('-')[-1])

		for sibling in siblings:
			sibling_sub_id = int(sibling.hierarchical_id.split('-')[-1])
			if sibling_sub_id == sub_id - 1:
				print()
				print()
				print(sibling.hierarchical_id, sibling.name)
				print()
				print()
				vals['precedent_project_id'] = sibling.id
				break

		return super(GanttView, self).create(vals)


	@api.onchange('hierarchical_id')
	def _onchange_hierarchical_id(self):
		print(self.hierarchical_id)

		if self.parent_id:
			sibling = self.env['viseo.project.project'].search([('parent_id', '=', self.parent_id.id)])
		else:
			sibling = self.env['viseo.project.project'].search([('parent_id', '=', False)])

		for pr in sibling:
			if (pr.hierarchical_id == self.hierarchical_id):
				pr.hierarchical_id = self.increment_hierarchical_id(pr.hierarchical_id)
				print()
				print(self.name)
				print(pr.name)
				print(pr.hierarchical_id)
				print()
				break


	def increment_hierarchical_id(self, hierarchical_id):
		incremented_sub_id = str(int(hierarchical_id[-1]) + 1)
		return hierarchical_id[:-1] + incremented_sub_id


	def compute_default_hierarchical_id(self):
		projects = self.env['viseo.project.project'].search([])
		for project in projects:
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

			# Find the next sibling based on hierarchical_id
			next_sibling = self.search([
				('parent_id', '=', project.parent_id.id),
				('hierarchical_id', '>', project.hierarchical_id),
			], order='hierarchical_id', limit=1)

			print(self.hierarchical_id)

			if next_sibling:
				project.next_project = next_sibling.id
			else:
				project.next_project = False
		print()
		print()
		print()
















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
	_order = 'hierarchical_id'
	date_start = fields.Date(string='Start', index=True, copy=False, tracking=True)

	hierarchical_id = fields.Char(
		string='Hierarchical ID',
		# compute='_compute_hierarchical_id',
		# store=True
	)

	def _compute_hierarchical_id(self):
		tasks = self.env['viseo.project.task'].search([])
		for task in tasks:
			project_id = task.viseo_project_id.hierarchical_id
			hierarchical_id = ''
			if task.parent_id.hierarchical_id != False:
				parent_hierarchical_id = task.parent_id.hierarchical_id
				if isinstance(task.id, int):
					sibling_count = tasks.search_count([('viseo_project_id', '=', task.viseo_project_id.id),('parent_id', '=', task.parent_id.id), ('id', '<=', task.id)])
					hierarchical_id = f'{parent_hierarchical_id}-{sibling_count}'
			else:
				if isinstance(task.id, int):
					root_count = tasks.search_count([('viseo_project_id', '=', task.viseo_project_id.id),('parent_id', '=', False), ('id', '<=', task.id)])
					if root_count:
						hierarchical_id = f'{project_id}-{root_count}'
			task.hierarchical_id = hierarchical_id



	@api.onchange('hierarchical_id')
	def recompute_next_task_id(self):
		next_task = self.env['viseo.project.task'].search([('viseo_project_id', '=', self.viseo_project_id.id),('parent_id', '=', self.parent_id.id)])
		for task in next_task:
			print()
			print()
			print()
			print('parent', task.parent_id.hierarchical_id)
			print()
			print()
			print()
			print()
			print(task.hierarchical_id[-1])






	@api.model
	def create(self, vals):
		if vals.get('parent_id'):
			parent = self.env['viseo.project.task'].browse(vals['parent_id'])
			siblings = self.env['viseo.project.task'].search([('parent_id', '=', vals['parent_id']), ('viseo_project_id', '=', vals['viseo_project_id'])])
			sibling_count = len(siblings)
			hierarchical_id = f'{parent.hierarchical_id}-{sibling_count + 1}'

		else:
			project_parent = self.env['viseo.project.project'].browse(vals['viseo_project_id'])
			parent_hierarchical_id = project_parent.hierarchical_id

			print(project_parent, parent_hierarchical_id)
			siblings = self.env['viseo.project.task'].search([('parent_id', '=', False), ('viseo_project_id', '=', vals['viseo_project_id'])])
			root_count = len(siblings)
			hierarchical_id = f'{parent_hierarchical_id}-{root_count + 1}'
			print(hierarchical_id)

		vals['hierarchical_id'] = hierarchical_id
	
		# context: no_log, because subtype already handle this
		context = dict(self.env.context)

		# for default stage
		if vals.get('viseo_project_id') and not context.get('default_viseo_project_id'):
			context['default_viseo_project_id'] = vals.get('viseo_project_id')

		# user_id change: update date_assign
		if vals.get('user_id'):
			vals['date_assign'] = fields.Datetime.now()

		# Stage change: Update date_end if folded stage and date_last_stage_update
		if vals.get('stage_id'):
			vals.update(self.update_date_end(vals['stage_id']))
			vals['date_last_stage_update'] = fields.Datetime.now()

		# substask default values
		if vals.get('parent_id'):
			for fname, value in self._subtask_values_from_parent(vals['parent_id']).items():
				if fname not in vals:
					vals[fname] = value

		task = super(ViseoTask, self.with_context(context)).create(vals)
		if task.viseo_project_id.privacy_visibility == 'portal':
			task._portal_ensure_token()



		return task





	






