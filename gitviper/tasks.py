from os import walk
import os.path as osp

from gitviper.settings import settings as s
from gitviper.colors import *
from gitviper.gitconnector import connection

import gitviper.utilities as utils

spacing = "  "
taskspacing = "  "

def list_tasks():
	counter_dict = {}

	for task in s.tasks:
		counter_dict[task.value] = 0

	files = utils.get_files()

	for f in files:
		count_tasks(osp.join(f[0], f[1]), counter_dict)

	lines = {}

	max_task_chars = 0
	max_digits = 0

	for task in s.tasks:
		if counter_dict[task.value] > 0:
			max_task_chars = max(len(task.representation), max_task_chars)
			max_digits = max(len(str(counter_dict[task.value])), max_digits)

	for task in s.tasks:
		if counter_dict[task.value] == 0:
			continue
		color = task.bgcolor
		line = BLACK + color + " " + task.representation.ljust(max_task_chars) + spacing + str(counter_dict[task.value]).rjust(max_digits) + " " + RESET + taskspacing

		if task.row not in lines:
			lines[task.row] = "  " # initial spacing

		lines[task.row] += line

	# print lines

	first_line_done = False

	for line_key in sorted(lines, reverse = False):

		# don't add empty line for fist line
		if first_line_done:
			print()

		print(lines[line_key])

		first_line_done = True


	return len(lines) > 0

def count_tasks(filename, counter_dict):
	with open(filename, 'r') as myfile:
		try:
			filestream = myfile.read().lower()

			for task in s.tasks:
				counter_dict[task.value] += filestream.count(task.value.lower())

		except UnicodeDecodeError:
			#print(RED, "Could not read", filename, RESET)
			pass
