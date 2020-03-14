from git import Repo, Commit

import gitviper.utilities as util
import gitviper.gui as gui
from gitviper.colors import *

from gitviper.gitconnector import connection

# Constants
spacing_sub_header = ' ' * 2
spacing_files = ' ' * 4
BINARY_KEYWORD = 'Bin'

STAGED = 'staged'
UNSTAGED = 'unstaged'

# Just to avoid passing variables multiple time through various functions...
class Variables: pass
values = Variables()
values.max_value = 0 # don't reset when for switching between staged/unstaged
values.max_character_num = 0
values.max_digits = 0
values.max_used_space = 0

def list_status():
	if connection.repo.is_dirty() or len(connection.repo.untracked_files) > 0:
		_list_status()

		return True

	return False

def _list_status():
	gui.print_header("Status", BG_GREEN)
	generate_num_stats()

	list_staged_files()
	list_unstaged_files()
	list_untracked_files()
	list_unmerged_paths()

def generate_num_stats():
	global changed_lines_by_file
	changed_lines_by_file = {}

	s_files = connection.repo.git.diff('--numstat', '--staged').split('\n')
	changed_lines_by_file['staged'] = _generate_num_stats(s_files)

	s_files = connection.repo.git.diff('--numstat').split('\n')
	changed_lines_by_file['unstaged'] = _generate_num_stats(s_files)

def _generate_num_stats(s_files):
	changed_lines = {}
	has_bin = False

	for s in s_files:
		*line_data, name = s.split('\t')
		try:
			adds, removes = [int(v) for v in line_data]
		except:
			adds, removes = [-1, -1]
			has_bin = True
		changed_lines[name] = [adds, removes]


		sum_value = adds + removes
		values.max_value = max(values.max_value, sum_value)
		sum_str_length = len(str(values.max_value))
		values.max_character_num = max(values.max_character_num, len(name))
		values.max_digits = sum_str_length
		values.max_used_space = max(values.max_used_space, len(name) + sum_str_length)

	if has_bin:
		values.max_digits = max(values.max_digits, len(BINARY_KEYWORD))

	return changed_lines

def list_staged_files():
	try:
		flip = True
		staged_diffs = connection.repo.index.diff(connection.repo.head.commit)
	except ValueError: # if there are no commits yet, there is nothing to compare against
		flip = False
		staged_diffs = connection.repo.index.diff(None, staged=True)

	if len(staged_diffs) > 0 and _count_real_diffs(staged_diffs) > 0:
		print_sub_header("Staged files", None)

		_list_diffs(staged_diffs, flip, STAGED)

def list_unstaged_files():
	unstaged_diffs = connection.repo.index.diff(None)

	if len(unstaged_diffs) > 0:
		print_sub_header("Unstaged files", None)

		_list_diffs(unstaged_diffs, False, UNSTAGED)

def list_untracked_files():
	u_files = connection.repo.git.ls_files("--others", "--directory", "--exclude-standard", "--no-empty-directory").split('\n')
	u_files = list(filter(None, u_files)) # Strip empty lines, only needed for last new-line

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

def _list_diffs(diffs, staged_files, staged):
	iterate_diffs(diffs.iter_change_type('A'), "deleted" if staged_files else "added", staged)
	iterate_diffs(diffs.iter_change_type('D'), "new file" if staged_files else "deleted", staged)
	iterate_diffs(diffs.iter_change_type('R'), "renamed", staged)
	iterate_diffs(diffs.iter_change_type('M'), "modified", staged)

# HACK this prevents subcatgory 'staged' showing up if there are unmerged paths
# because diffs contain one element (per unmerged path?)
# but when iterating over 'A', 'D', 'R' and 'M'
# there are no changes...
def _count_real_diffs(diffs):
	return len(list(diffs.iter_change_type('A'))) + len(list(diffs.iter_change_type('D'))) + len(list(diffs.iter_change_type('R'))) + len(list(diffs.iter_change_type('M')))

def iterate_diffs(diffs, modifier, staged):
	if staged == STAGED:
		color = GREEN
		changed_lines = changed_lines_by_file[STAGED]
	elif staged == UNSTAGED:
		color = RED
		changed_lines = changed_lines_by_file[UNSTAGED]


	texts = []
	max_text_length = 1
	for d in diffs:
		text = f"{color}{spacing_files}{modifier}:\t{d.a_path.ljust(values.max_character_num)}{RESET} | "
		texts.append({
			'path': d.a_path,
			'text': text
		})

		max_text_length = max(max_text_length, len(text)) # FIXME is including white space for ANSI color code sequences, which will result in a padding to the window border

	# Calculate relative size
	w = util.get_window_size()
	space_for_symbols = w.x - max_text_length # FIXME will break if text is bigger than window width

	factor = values.max_value / float(space_for_symbols)
	factor = max(1, factor)

	# Create symbol line
	for text in texts:
		added_lines_num = changed_lines[text['path']][0]
		deleted_lines_num = changed_lines[text['path']][1]

		adds = '+' * (int(round(added_lines_num / factor)))
		deletes = '-' * (int(round(deleted_lines_num / factor)))

		# Show at least one symbol if addition / deletion occured, regardless of relative scale to biggest changes
		if added_lines_num > 0 and adds == '':
			if len(deletes) == space_for_symbols:
				deletes = deletes[:-1]
			adds = '+'

		if deleted_lines_num > 0 and deletes == '':
			if len(adds) == space_for_symbols:
				adds = adds[:-1]
			deletes = '-'

		# Show symbol for binary files
		sum_info = added_lines_num + deleted_lines_num
		if added_lines_num + deleted_lines_num < 0:
			sum_info = BINARY_KEYWORD

		symbols_text = f"{str(sum_info).rjust(values.max_digits)} {GREEN}{adds}{RESET}{RED}{deletes}{RESET}"
		print(f"{text['text']}{symbols_text}")

def print_sub_header(text, color):
	print()
	if color:
		print(spacing_sub_header + color + text + RESET)
	else:
		print(spacing_sub_header + text)

def set_color(color):
	print(color, end="")
