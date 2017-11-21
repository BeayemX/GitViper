import os
from os import walk
from gitviper.settings import settings

import datetime
import humanize

class Vector2:
	def __init__(self, x, y):
		self.x = x
		self.y = y

def get_window_size():
	rows, columns = os.popen('stty size', 'r').read().split()
	return Vector2(columns, rows)

def get_files():
	files = []

	for (dirpath, dirnames, filenames) in walk(os.getcwd()):
		dirnames[:] = [d for d in dirnames if d not in settings.excluded_directories]

		# TODO use generator?
		for f in filenames:
			for exf in settings.excluded_files:
				if exf in f:
					break
			else:
				files.append((dirpath, f))
	return files

def get_relative_date(time):
	t = datetime.datetime.fromtimestamp(time)
	return humanize.naturaltime(t)