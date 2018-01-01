from git import Repo, Commit

import gitviper.gui as gui
from gitviper.colors import *

from gitviper.gitconnector import connection

spacing_sub_header = "  "
spacing_files = "    "

def list_status():
	if connection.repo.is_dirty() or len(connection.repo.untracked_files) > 0:
		_list_status()

		return True

	return False

def _list_status():
	gui.print_header("Status", BG_GREEN)
	list_staged_files()
	list_unstaged_files()
	list_untracked_files()
	list_unmerged_paths()

def list_staged_files():
	try:
		flip = True
		staged_diffs = connection.repo.index.diff(connection.repo.head.commit)
	except ValueError:
		flip = False
		staged_diffs = connection.repo.index.diff(None, staged=True)

	if len(staged_diffs) > 0:
		print_sub_header("Staged files", None)

		set_color(GREEN)
		_list_diffs(staged_diffs, flip)
		set_color(RESET)

def list_unstaged_files():
	unstaged_diffs = connection.repo.index.diff(None)

	if len(unstaged_diffs) > 0:
		print_sub_header("Unstaged files", None)

		set_color(RED)
		_list_diffs(unstaged_diffs, False)
		set_color(RESET)

def list_untracked_files():
	u_files = connection.repo.untracked_files

	if len(u_files) > 0:
		print_sub_header("Untracked files", None)

		for f in u_files:
			print(spacing_files + YELLOW + f + RESET)

def list_unmerged_paths():
	unmerged_blobs = connection.repo.index.unmerged_blobs()

	if len(unmerged_blobs) > 0:
		print_sub_header("Unmerged paths", None)

		for ublob in unmerged_blobs:
			print(BOLD + MAGENTA + spacing_files + ublob + RESET)

def _list_diffs(diffs, staged_files):
	iterate_diffs(diffs.iter_change_type('A'), "deleted" if staged_files else "added")
	iterate_diffs(diffs.iter_change_type('D'), "new file" if staged_files else "deleted")
	iterate_diffs(diffs.iter_change_type('R'), "renamed")
	iterate_diffs(diffs.iter_change_type('M'), "modified")

def iterate_diffs(diffs, text):
	diff_iter = list(diffs)

	if len(diff_iter) > 0:
		for d in diff_iter:
			print(spacing_files + text + ":\t" + d.a_path)

def print_sub_header(text, color):
	print()
	if color:
		print(spacing_sub_header + color + text + RESET)
	else:
		print(spacing_sub_header + text)

def set_color(color):
	print(color, end="")