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

# TODO Put these settings into a config file and/or make available through CLI
conf = {
	'list_occurences': True,
	'show_staged': True,
	'show_unstaged': True,
	'show_resolved': True
}

def list_tasks_of_diff(list_occurences):
	conf['list_occurences'] = list_occurences
	try:
		_list_tasks_of_diff()
	except ValueError as e:
		print("Could not list tasks of diff!")
		print(e)

def _list_tasks_of_diff():
	t = connection.repo.head.commit
	if conf['show_staged']:
		staged_diff = connection.repo.git.diff(t, '--color=always', '--staged').split('\n')
	if conf['show_unstaged']:
		unstaged_diff = connection.repo.git.diff(t, '--color=always').split('\n') # FIXME this includes staged changes. Maybe compare against sth else than 'head.commit'

	# Remove staged lines from unstaged diff
	if conf['show_staged'] and conf['show_unstaged']:
		for diff_line in staged_diff:
			for unstaged_diff_line in unstaged_diff:
				if diff_line == unstaged_diff_line:
					unstaged_diff.remove(diff_line)

	def _sanitize(lines):
		additions = []
		deletions = []

		for line in lines:
			if line.startswith(GREEN):
				new_line = line.lstrip(GREEN)[1:]
				additions.append(new_line)
			elif line.startswith(RED):
				new_line = line.lstrip(RED)[1:]
				deletions.append(new_line)

		return additions, deletions

	if conf['show_staged']:
		staged_additions, staged_deletions = _sanitize(staged_diff)
	if conf['show_unstaged']:
		unstaged_additions, unstaged_deletions = _sanitize(unstaged_diff)

	has_content = False
	staged_has_content = False
	unstaged_has_content = False

	# List staged Tasks
	if conf['show_staged']:
		staged_has_content = create_stage_area("Staged", f"{BG_RED}{BOLD}{WHITE}", staged_additions, staged_deletions, f"{BOLD}{RED}", f"{BOLD}{GREEN}")
		if staged_has_content:
			print()

	# List unstaged Tasks
	if conf['show_unstaged']:
		unstaged_has_content = create_stage_area("Unstaged", f"{BG_YELLOW}{BOLD}{BLACK}", unstaged_additions, unstaged_deletions, f"{BOLD}{YELLOW}", f"{BOLD}{YELLOW}")
		if unstaged_has_content:
			print()

	has_content = staged_has_content | unstaged_has_content

	# Finalize Tasks area
	if has_content:
		draw_separator()

def create_stage_area(title, title_color, additions, deletions, add_color, del_color):
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

		if conf['show_resolved']:
			for line in deletions:
				if task.value in line:
					deleted_counter_dict[task.value] += 1
					deleted_not_empty = True


	def list_tasks_in_changes(lines):
		win_x = utils.get_window_size().x
		for task in task_loader.tasks:
			# occurence_happened = False
			for line in lines:
				if task.value in line:
					# occurence_happened = True
					l = remove_color_codes_from_string(line).strip()
					line_parts = l.split(task.value, 1)
					l = f"   {line_parts[0]}{BOLD}{task.color}{task.value}{RESET}{line_parts[1]}"
					if len(remove_color_codes_from_string(l)) > win_x:
						l = l[:win_x + 3] + "..."
						remove_color_codes_from_string

					print(f"{RESET}{WHITE}{l}")

	def _print_task_area(title, color, dictionary, changes, use_full_line=False):
		displayed_title = f' {title}'
		if use_full_line:
			line = displayed_title + ' ' * (utils.get_window_size().x - len(displayed_title))
		else:
			line = displayed_title + '  '

		print(f"{color}{line}{RESET}")

		# print_tasks(dictionary) # Show badges

		if conf['list_occurences']:
			list_tasks_in_changes(changes)

	# todo
	has_content = added_not_empty or (conf['show_resolved'] and deleted_not_empty)
	if has_content:
		print(f"{title_color}  {title}  {RESET}")

	if added_not_empty:
		_print_task_area("[ New ]", add_color, added_counter_dict, additions)

	if conf['show_resolved'] and deleted_not_empty:
		if added_not_empty:
			#print()
			pass

		_print_task_area("[ Resolved ]", del_color, deleted_counter_dict, deletions)

	return has_content

def draw_separator():
	char = '='
	line = char * (utils.get_window_size().x // len(char))
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
