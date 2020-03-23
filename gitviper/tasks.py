from os import walk
import os.path as osp

from gitviper.task_loader import task_loader
from gitviper.colors import *
from gitviper.gitconnector import connection

import gitviper.utilities as utils

spacing = " " * 2
taskspacing = " " * 2
initial_spacing = " " * 2

# Configuration
DISPLAY_RESOLVED_TASKS = True

def list_tasks_of_diff(list_occurences):
	try:
		_list_tasks_of_diff(list_occurences)
	except ValueError as e:
		print("Could not list tasks of diff!")
		print(e)

def _list_tasks_of_diff(list_occurences):
	t = connection.repo.head.commit.tree
	x = connection.repo.git.diff(t, '--color=always').split('\n')
	y = connection.repo.git.diff(t, '--color=always', '--staged').split('\n')

	z = y # list only for staged
	z = x # list staged and unstaged

	final_lines = []
	additions = []
	deletions = []

	for line in z:
		if line.startswith(GREEN):
			new_line = line.lstrip(GREEN)[1:]
			final_lines.append(new_line)
			additions.append(new_line)
		elif line.startswith(RED):
			new_line = line.lstrip(RED)[1:]
			final_lines.append(new_line)
			deletions.append(new_line)

	added_counter_dict = {}
	deleted_counter_dict = {}

	for task in task_loader.tasks:
		added_counter_dict[task.value] = 0
		deleted_counter_dict[task.value] = 0

	added_not_empty = False
	deleted_not_empty = False

	for task in task_loader.tasks:
		for line in additions:
			if task.value in line:
				added_counter_dict[task.value] += 1
				added_not_empty = True
		if DISPLAY_RESOLVED_TASKS:
			for line in deletions:
				if task.value in line:
					deleted_counter_dict[task.value] += 1
					deleted_not_empty = True


	def list_tasks_in_changes(lines):
		for task in task_loader.tasks:
			# occurence_happened = False
			for line in lines:
				if task.value in line:
					# occurence_happened = True
					l = remove_color_codes_from_string(line).strip()
					line_parts = l.split(task.value, 1)
					l = f"  {line_parts[0]}{BOLD}{task.color}{task.value}{RESET}{line_parts[1]}"
					print(f"{RESET}{WHITE}{l}")
			# if occurence_happened:
				# print()


	if added_not_empty:
		# Highlight line
		title =  '  Newly introduced tasks'
		line = title + ' ' * (utils.get_window_size().x - len(title))
		print(f"{BG_RED}{BOLD}{line}{RESET}")
		print()

		# Print actual Tasks
		print_tasks(added_counter_dict)

		if list_occurences:
			list_tasks_in_changes(additions)

		#title =  ''
		#line = title + ' ' * (utils.get_window_size().x - len(title))
		#print(f"{BG_RED}{line}{RESET}")

		# Highlight line
		#print()

	if DISPLAY_RESOLVED_TASKS and deleted_not_empty:
		# Highlight line
		title =  '  Resolved tasks'
		line = title + ' ' * (utils.get_window_size().x - len(title))
		if added_not_empty:
			print()

		print(f"{BG_GREEN}{BLACK}{line}{RESET}")
		print()

		# Print actual Tasks
		print_tasks(deleted_counter_dict)

		if list_occurences:
			list_tasks_in_changes(deletions)


		#title =  ''
		#line = title + ' ' * (utils.get_window_size().x - len(title))
		#print(f"{BG_GREEN}{line}{RESET}")

		# Highlight line
		#print()

	if added_not_empty or (DISPLAY_RESOLVED_TASKS and deleted_not_empty):
		line = '_' * utils.get_window_size().x
		print(f"{WHITE}{line}{RESET}")
		print()

def list_tasks():
	counter_dict = {}

	for task in task_loader.tasks:
		counter_dict[task.value] = 0

	files = utils.get_files()

	for f in files:
		count_tasks(osp.join(f[0], f[1]), counter_dict)

	print_tasks(counter_dict)

def print_tasks(counter_dict):
	lines = {}

	max_task_chars = 0
	max_digits = 0

	for task in task_loader.tasks:
		if counter_dict[task.value] > 0:
			max_task_chars = max(len(task.representation), max_task_chars)
			max_digits = max(len(str(counter_dict[task.value])), max_digits)

	for task in task_loader.tasks:
		if counter_dict[task.value] == 0:
			continue
		color = task.bgcolor
		line = BLACK + color + " " + task.representation.ljust(max_task_chars) + spacing + str(counter_dict[task.value]).rjust(max_digits) + " " + RESET + taskspacing

		if task.row not in lines:
			lines[task.row] = initial_spacing

		lines[task.row] += line

	# Print lines
	for line_key in sorted(lines, reverse = False):
		print(lines[line_key])
		print()

	return len(lines) > 0

def count_tasks(filename, counter_dict):
	with open(filename, 'r') as myfile:
		try:
			filestream = myfile.read()

			for task in task_loader.tasks:
				counter_dict[task.value] += filestream.count(task.value)

		except UnicodeDecodeError:
			#print(RED, "Could not read", filename, RESET)
			pass
