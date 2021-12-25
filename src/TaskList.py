import os
import os.path as osp
import argparse

from gitviper.colors import *

import gitviper.utilities as utils
from gitviper.task_loader import task_loader


occurences_dict = {}
spacing = "   "
window_padding = " "


class Occurence:
    def __init__(self, path, filename, linenumber, linecontent):
        self.filename = filename
        self.path = path
        self.linenumber = linenumber
        self.linecontent = linecontent


class TaskListLineEntry():
    def __init__(self, linecontent = "", path = "", linenumber = ""):
        self.linecontent = linecontent
        self.path = path
        self.linenumber = linenumber


def fill_dictionary(task, file):
    occurences = []
    fullpath = osp.join(file[0], file[1])
    with open(fullpath, 'r') as myFile:
        try:
            for num, line in enumerate(myFile, 1):
                if task.value in line:
                    occurences.append([num, line])
        except UnicodeDecodeError:
            pass

    if len(occurences) > 0:
        for o in occurences:
            occ = Occurence(file[0], file[1], o[0], o[1])
            occurences_dict[task].append(occ)


def split_stream(occurence, task): # TODO rename
    stream = occurence.linecontent
    key = task.value

    last_index = 0
    all_lines = []

    stream = stream.strip()

    # strip commenting symbols
    if task_loader.strip_comment_symbols:
        stream = stream.replace("#", "")
        stream = stream.replace("//", "")
        stream = stream.replace("/*", "")
        stream = stream.replace("\t", " ")
        stream = stream.strip()


    stream_split = stream.split(key)

    for s in stream_split:
        task_list_line_entry = TaskListLineEntry()


        final_string = ""
        start_index = stream.find(s, last_index)
        s_length = len(s)

        task_start_idx = start_index - len(key) # the task keywords is before 's'
        task_end_idx = start_index

        # line ends with task keyword?
        if start_index + len(key) == len(stream):
            #raise Exception(BOLD + RED + "when does this happen?" + RESET)
            task_end_idx = len(stream)
            task_start_idx = task_end_idx - len(key)
            start_index = task_end_idx

        last_index = start_index + s_length # has to be before 'continue'

        # every logic part should be before this, only printing afterwards
        if task_start_idx < 0:
            continue

        highlighted_task = BOLD + task.color + task.value + RESET

        before = stream[ 0 : start_index - len(key)]
        after = stream[start_index : ]

        # add to data used for creating table
        if task_loader.show_paths_for_task_list == args.toggle_paths:
            path = occurence.path.replace(os.getcwd(), "") + "/"
            path = path.lstrip("/")
        else:
            path = ""

        task_list_line_entry.linecontent = before + highlighted_task + after

        if task_loader.show_paths_for_task_list == args.toggle_paths:
            task_list_line_entry.path = path + BOLD + task.color + occurence.filename.rjust(0).strip() + RESET
        else:
            task_list_line_entry.path = path + occurence.filename.rjust(0).strip()

        task_list_line_entry.linenumber = (str(occurence.linenumber))


        all_lines.append(task_list_line_entry)

        # HACK to avoid duplicate lines when 'task.key == linecontent'
        hack_check = ","
        if hack_check.join(stream_split) == hack_check:
            break

    return all_lines


def list_tasks(cli_tasks):
    # TODO should avoid adding unused Tasks in the first place instead of adding them and then clearing the list
    if args.ignore_conf:
        task_loader.clear_tasks()

    if cli_tasks != None:
        from gitviper.task import Task
        for cli_task in cli_tasks:
            task_loader.add_task(Task(cli_task, {}))

    # Initialize dict
    for k in task_loader.tasks:
        occurences_dict[k] = []

    # Get files as list
    files = utils.get_files()

    # Fill dictionary
    for task in task_loader.tasks:
        for f in files:
            fill_dictionary(task, f)

    # Create list of dict entries and ignore empty task-entries
    occurences_dict_list = []
    for key in occurences_dict:
        if len(occurences_dict[key]) == 0:
            # TODO use some sort of Debug print to be able to show when using --debug
            # print("No tasks for: " + key.representation)
            continue
        else:
            occurences_dict_list.append((key, occurences_dict[key]))

    # sort list by priority
    def getKey(item):
        return item[0].priority
    occurences_dict_sorted_by_priority = sorted(occurences_dict_list, reverse=True, key=getKey)

    # print table
    for kv in occurences_dict_sorted_by_priority:
        task = kv[0] # Task
        occurence_list = kv[1] # Occurence []
        task_list_line_entries = []


        for o in occurence_list:
            for line in split_stream(o, task):
                task_list_line_entries.append(line)

        # find max column widths
        substitutes = [0] * 4 # substitutes for invisible characters
        substitutes[1] = len(BOLD + RESET) # for highlighting tasks # FIXME adjust to new format, individual color per Task?

        if task_loader.show_paths_for_task_list == args.toggle_paths:
            substitutes[2] = len(BOLD + BLUE + RESET) # for highlighting filename if also showing path
        else:
            substitutes[2] = 0


        max_widths = [0] * 3
        for task_list_line_entry in task_list_line_entries:
            max_widths[0] = max(max_widths[0], len(task_list_line_entry.linecontent))
            max_widths[1] = max(max_widths[1], len(task_list_line_entry.path))
            max_widths[2] = max(max_widths[2], len(task_list_line_entry.linenumber))

        if task_loader.show_paths_for_task_list == args.toggle_paths:
            max_widths[1] -= substitutes[2]

        line_beginning_spacing = "  "
        #max_widths[0] = len(line_beginning_spacing)

        # clamp to window width
        s = len(spacing)
        availablespace = utils.get_window_size().x - len(line_beginning_spacing) - s - max_widths[1] - s - max_widths[2] - s - len(window_padding) + substitutes[1] + s + 6 # the last ' + s + 2' is for setting [0] to 'line_beginning_spacing' and add whitespace to the right side
        max_widths[0] = availablespace

        print(" " + task.color + BOLD + task.representation + " [" + str(len(task_list_line_entries)) + "]" + RESET)
        print()

        for task_list_line_entry in task_list_line_entries:
            if len(task_list_line_entry.linecontent) > max_widths[0]:
                task_list_line_entry.linecontent = task_list_line_entry.linecontent[:max_widths[0] - 3] + "..."

            taskword = line_beginning_spacing
            line = task_list_line_entry.linecontent[ : max_widths[0]].ljust(max_widths[0]) + spacing
            filename = task_list_line_entry.path.ljust(max_widths[1] + substitutes[2]) + spacing
            linenumber = task_list_line_entry.linenumber.rjust(max_widths[2])


            # TODO use python3.6 f-strings
            text = "%s%s%s%s"%(taskword,line, filename,linenumber)
            print(text)

        print()

print(" " + BG_WHITE + BLACK + "  Tasks  " + RESET)
print()

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--toggle-paths", action='store_false', help="execute with inverted show-paths property")
parser.add_argument("-a", "--additional-tasks", nargs="*")
parser.add_argument("-i", "--ignore-conf", action="store_true")

args = parser.parse_args()

try:
    list_tasks(args.additional_tasks)
except KeyboardInterrupt:
    print(BG_RED + WHITE + " Execution canceled... " + RESET)
except BrokenPipeError: # occurs sometimes after quitting less when big git-logs are displayed
    pass

