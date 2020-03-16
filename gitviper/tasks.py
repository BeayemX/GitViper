from os import walk
import os.path as osp

from gitviper.task_loader import task_loader
from gitviper.colors import *
from gitviper.gitconnector import connection

import gitviper.utilities as utils

spacing = " " * 2
taskspacing = " " * 2
initial_spacing = " " * 2

def list_tasks_of_diff(list_occurences):
	t = connection.repo.head.commit.tree
	x = connection.repo.git.diff(t, '--color=always').split('\n')
	y = connection.repo.git.diff(t, '--color=always', '--staged').split('\n')

	z = y # list only for staged
	z = x # list staged and unstaged

	final_lines = []

	for line in z:
		if line.startswith(GREEN):
			new_line = line.lstrip(GREEN)[1:]
			final_lines.append(new_line)
		elif line.startswith(RED):
			new_line = line.lstrip(RED)[1:]
			final_lines.append(new_line)

	counter_dict = {}

	for task in task_loader.tasks:
		counter_dict[task.value] = 0

	not_empty = False
	for task in task_loader.tasks:
		for line in final_lines:
			if task.value in line:
				counter_dict[task.value] += 1
				not_empty = True

	def list_tasks_in_changes():
		for task in task_loader.tasks:
			occurence_happened = False
			for line in final_lines:
				if task.value in line:
					occurence_happened = True
					l = remove_color_codes_from_string(line).strip()
					line_parts = l.split(task.value, 1)
					l = f"  {line_parts[0]}{BOLD}{task.color}{task.value}{RESET}{line_parts[1]}"
					print(f"{RESET}{WHITE}{l}")
			if occurence_happened:
				print()


	if not_empty:
		# Highlight line
		line = ' ' * utils.get_window_size().x
		print(f"{BG_RED}{line}{RESET}")
		print()

		# Print actual Tasks
		print_tasks(counter_dict)

		if list_occurences:
			list_tasks_in_changes()

		# Highlight line
		print(f"{BG_RED}{line}{RESET}")
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
