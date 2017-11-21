from git import GitCommandError

from gitviper.gitconnector import connection
import gitviper.gitstuff as gitstuff

import gitviper.gui as gui
import gitviper.utilities as utilities

from gitviper.colors import *
from gitviper.settings import settings as s

spacing = "  "

def list_logs(num):
	if show_logs():
		log(num)
		print()

def show_logs():
	try:
		list(connection.repo.iter_commits(connection.repo.active_branch))
	except GitCommandError:
		return False

	return True

def log(max_commit_count):
	branch = connection.repo.active_branch
	num_commits = len(list(connection.repo.iter_commits(branch)))
	commits = list(connection.repo.iter_commits(branch, max_count = max_commit_count))

	info_text = ""

	# add ahead / behind info if there is a remote branch
	if gitstuff.remote_exists(branch):
		info_text = CYAN + "[ "
		info_text += branch.name
		info_text += " → "
		info_text += branch.tracking_branch().name

		ahead = gitstuff.get_ahead(branch)
		behind = gitstuff.get_behind(branch)

		if ahead > 0 or behind > 0:
			info_text += BOLD
			if ahead > 0:
				info_text += " push(" + str(ahead) + ")"
			if behind > 0:
				info_text += " pull(" + str(behind) + ")"

			info_text += BOLD_OFF
			info_text += CYAN

		info_text += " ]" + RESET
	else:
		info_text += CYAN + "[ " + branch.name + " ] " + RESET
		info_text += YELLOW + " <local branch> " + RESET

	gui.print_header("Commits (" + str(num_commits) + ")", BG_CYAN, info_text)

	# generate commit arrays
	commit_arrays = []
	for commit in commits:
		commit_arrays.append(commit_to_string(commit))

	# check if all commits are from the same author
	multi_author = s.always_show_authors

	if not s.always_show_authors:
		if len(commit_arrays) > 0:
			initial_author = commit_arrays[0][1]
			for commit in commit_arrays:
				if commit[1] != initial_author:
					multi_author = True
					break

	# calculate table
	max_col_widths = [0, 0, 0]
	for commit in commit_arrays:
		for i in range(len(max_col_widths)):
			max_col_widths[i] = max(max_col_widths[i], len(commit[i] + spacing))

	# don't show author if all commits are from same author
	if not multi_author:
		max_col_widths[1] = 0

	# cap message length so there is no line break
	w = utilities.get_window_size()
	msg_length = int(w.x) - max_col_widths[0] - max_col_widths[1]

	max_col_widths[2] = msg_length

	for commit in commit_arrays:
		text = CYAN + commit[0].ljust(max_col_widths[0]) + RESET

		if multi_author:
			text += GREEN + commit[1].ljust(max_col_widths[1]) + RESET

		# highlight first word of each message
		msg = commit[2][:msg_length]
		msg = msg.split(" ")
		msg[0] = BOLD + msg[0] + RESET
		text += " ".join(msg)
		print(text)

def commit_to_string(commit):
	rel_date = utilities.get_relative_date(commit.committed_date)
	author = commit.author.name[:s.commit_author_max_length]
	msg = commit.message.split("\n")[0] # [:msg_length-1]

	return [rel_date, author, msg]