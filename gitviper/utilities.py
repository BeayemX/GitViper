import os
from os import walk
from gitviper.task_loader import task_loader

from datetime import datetime, timedelta
import humanize

class Vector2:
	def __init__(self, x, y):
		self.x = x
		self.y = y

def get_window_size():
	rows, columns = os.popen('stty size', 'r').read().split()
	return Vector2(int(columns), int(rows))

def get_files():
	files = []

	for (dirpath, dirnames, filenames) in walk(os.getcwd()):
		dirnames[:] = [d for d in dirnames if d not in task_loader.ignored_directories]

		# TODO use generator?
		for f in filenames:
			for exf in task_loader.ignored_files:
				if exf.casefold() in f.casefold():
					break
			else:
				files.append((dirpath, f))
	return files

def get_relative_date(time):
	return humanize.naturaltime(get_date(time))

def get_date(timestamp):
	return datetime.fromtimestamp(timestamp)

def is_date_older_than_days(date, days):
	return date < datetime.now() - timedelta(days=days)

def age_in_days(date):
	return (datetime.now() - date).days