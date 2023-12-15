



def indent(x):
		for i in range(x):
			print("", end="\t")

def print_data(project_ids, x=0):
	for project in project_ids:
		indent(x)
		print(project.id, '-', project.name)

		if project.task_ids:
			indent(x+1)
			print('- tasks :')
			for task in project.task_ids:
				indent(x+1)
				print(task.name)
			print('')
		else:
			indent(x+1)
			print('- tasks : NULL\n')

		if project.child_ids:
			indent( x+1 )
			print('* sub_project :')
			for sub_project in project.child_ids:
				print_data(sub_project, x=x+1)
				x -= 1
			print('')
		else:
			indent( x+1 )
			print('- sub_project : NULL\n')




