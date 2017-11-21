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

	line1 = " "
	line2 = "\n "

	max_task_chars = 0
	max_digits = 0

	for task in s.tasks:
		max_task_chars = max(len(task.representation), max_task_chars)
		max_digits = max(len(str(counter_dict[task.value])), max_digits)

	for task in s.tasks:
		if counter_dict[task.value] == 0:
			continue
		color = task.bgcolor
		line = color + BLACK + " " + task.representation.ljust(max_task_chars) + spacing + str(counter_dict[task.value]).rjust(max_digits) + " " + RESET + taskspacing
		if task.priority > 0:
			line1 += line
		else:
			line2 += line

	if len(line1.strip()) > 0:
		print(line1)
	if len(line2.strip()) > 0:
		print(line2)
	if len(line1.strip()) > 0 or len(line2.strip()) > 0:
		print()

def count_tasks(filename, counter_dict):
	with open(filename, 'r') as myfile:
		try:
			filestream = myfile.read().lower()

			for task in s.tasks:
				counter_dict[task.value] += filestream.count(task.value.lower())

		except UnicodeDecodeError:
			#print(RED, "Could not read", filename, RESET)
			pass
