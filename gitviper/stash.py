import gitviper.utilities as util

import gitviper.gui as gui

from gitviper.colors import *
from gitviper.gitconnector import connection

spacing = 2

def list_stash():
	if stash_exists():
		print_stash()

		return True

	return False

def stash_exists():
	return len(connection.repo.git.stash("list")) > 0

def print_stash():
	gui.print_header("Stash", BG_YELLOW)

	# get stash information from git
	repo = connection.repo
	refs = repo.head.repo.refs
	stash = refs["refs/stash"]
	stash_log = stash.log()
	stash_log.reverse()

	# create entry to be formated as table
	stash_list = []
	stash_counter = 0

	for s in stash_log:
		entry = []

		entry.append("stash@{" + str(stash_counter) + "}:")
		entry.append(util.get_relative_date(s.time[0]))
		entry.append(s.message)

		stash_list.append(entry)
		stash_counter += 1

	# print stash information as table

	# calculate max widths needed
	col_num = len(stash_list[0])
	max_col_widths = [0] * col_num

	for entry in stash_list:
		for i in range(col_num):
			max_col_widths[i] = max(max_col_widths[i], len(entry[i]) + spacing)

	# cap message length so there is no line break
	w = util.get_window_size()
	msg_length = int(w.x) - max_col_widths[0] - max_col_widths[1]

	# use max length
	max_col_widths[2] = msg_length
	for entry in stash_list:
		entry[2] = entry[2][:msg_length]

	# print table
	for entry in stash_list:
		text = ""

		text += YELLOW + entry[0].ljust(max_col_widths[0]) + RESET
		text += CYAN + entry[1].ljust(max_col_widths[1]) + RESET
		text += entry[2].ljust(max_col_widths[2])

		print(text)