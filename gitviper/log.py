from git import GitCommandError

from gitviper.gitconnector import connection
import gitviper.gitstuff as gitstuff

import gitviper.gui as gui
import gitviper.utilities as utilities

from gitviper.colors import *
from gitviper.settings import settings as s

spacing = "  "


class CommitListEntry:
	def __init__(self, date, relative_date, author, message):
		self.date = date
		self.relative_date = relative_date
		self.author = author
		self.message = message


def list_logs(num, max_days_old, separate_commits):
	if show_logs():
		log(num, max_days_old, separate_commits)

		return True

	return False

def show_logs():
	try:
		list(connection.repo.iter_commits(connection.repo.active_branch))
	except GitCommandError:
		return False

	return True

def log(max_commit_count, max_days_old, separate_commits):
	branch = connection.repo.active_branch
	num_commits = len(list(connection.repo.iter_commits(branch)))

	# when max_days_old is specified, max_commit_count will be ignored
	# but to increase performance it is still limited to 500
	if max_days_old > 0:
		max_commit_count = 500

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

			info_text += RESET # BOLD_OFF
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
			initial_author = commit_arrays[0].author
			for commit in commit_arrays:
				if commit.author != initial_author:
					multi_author = True
					break

	# limit all commits to commits newer than max_days_old
	counter = 0
	for commit in commit_arrays:
		if max_days_old > 0:
			if utilities.is_date_older_than_days(commit.date, max_days_old):
				break
		counter += 1
	commit_arrays = commit_arrays[ 0 : counter ]

	# calculate table
	max_col_widths = [0, 0, 0]
	for commit in commit_arrays:
		max_col_widths[0] = max(max_col_widths[0], len(commit.relative_date + spacing))
		max_col_widths[1] = max(max_col_widths[1], len(commit.author + spacing))
		max_col_widths[2] = max(max_col_widths[2], len(commit.message + spacing))

	# don't show author if all commits are from same author
	if not multi_author:
		max_col_widths[1] = 0

	# cap message length so there is no line break
	w = utilities.get_window_size()
	msg_length = int(w.x) - max_col_widths[0] - max_col_widths[1]

	# store max needed length for commit before adjusting length for messages
	max_commit_length = max_col_widths[0] + max_col_widths[1] + max_col_widths[2] - len(spacing)
	max_commit_length = min(max_commit_length, int(w.x))
	max_col_widths[2] = msg_length

	last_day_age = utilities.age_in_days(commit_arrays[0].date)

	for commit in commit_arrays:
		# detect new day
		if separate_commits:
			if last_day_age != utilities.age_in_days(commit.date):
				last_day_age = utilities.age_in_days(commit.date)
				print(CYAN + "-" * max_commit_length + RESET)

		# actually print commit entries
		text = CYAN + commit.relative_date.ljust(max_col_widths[0]) + RESET

		if multi_author:
			text += GREEN + commit.author.ljust(max_col_widths[1]) + RESET

		# highlight first word of each message
		msg = commit.message # [:max_col_widths[2]]

		if len(msg) > max_col_widths[2]:
			msg = msg[:max_col_widths[2]-3] + "..."

		msg = msg.split(" ")
		msg[0] = BOLD + msg[0] + RESET
		text += " ".join(msg)
		print(text)

def commit_to_string(commit):
	rel_date = utilities.get_relative_date(commit.committed_date)
	date = utilities.get_date(commit.committed_date)
	author = commit.author.name[:s.commit_author_max_length]
	msg = commit.message.split("\n")[0] # [:msg_length-1]

	return CommitListEntry(date, rel_date, author, msg)