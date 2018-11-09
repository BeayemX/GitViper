import os
import os.path as osp
import argparse

from gitviper.colors import *

import gitviper.utilities as utils
from gitviper.settings import settings

occurences_dict = {}
spacing = "   "
window_padding = " "


class Occurence:
    def __init__(self, path, filename, linenumber, linecontent):
        self.filename = filename
        self.path = path
        self.linenumber = linenumber
        self.linecontent = linecontent

def fill_dictionary(task, file):
    occurences = []
    fullpath = osp.join(file[0], file[1])
    with open(fullpath, 'r') as myFile:
        try:
            for num, line in enumerate(myFile, 1):
                if task.value in line.lower():
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
    if settings.strip_comment_symbols:
        stream = stream.replace("#", "")
        stream = stream.replace("//", "")
        stream = stream.replace("/*", "")
        stream = stream.replace("\t", " ")
        stream = stream.strip()


    stream_split = stream.lower().split(key.lower())

    for s in stream_split:
        real_value_entry = []

        final_string = ""
        start_index = stream.lower().find(s, last_index)
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

        orig_task = BOLD + task.color + stream[task_start_idx : task_end_idx] + RESET

        before = stream[ 0 : start_index - len(key)]
        after = stream[start_index : ]

        # add to data used for creating table
        if settings.show_paths_for_task_list == args.toggle_paths:
            path = occurence.path.replace(os.getcwd(), "") + "/"
            path = path.lstrip("/")
        else:
            path = ""

        real_value_entry.append(window_padding + task.representation) # TODO remove, not used any more
        real_value_entry.append(before + orig_task + after)

        if settings.show_paths_for_task_list == args.toggle_paths:
            real_value_entry.append(path + BOLD + task.color + occurence.filename.rjust(0).strip() + RESET)
        else:
            real_value_entry.append(path + occurence.filename.rjust(0).strip())

        real_value_entry.append(str(occurence.linenumber))


        all_lines.append(real_value_entry)

    return all_lines


def list_tasks(cli_tasks):
    # TODO should avoid adding unused Tasks in the first place instead of adding them and then clearing the list
    if args.ignore_conf:
        settings.clear_tasks()

    if cli_tasks != None:
        from gitviper.task import Task
        for cli_task in cli_tasks:
            settings.add_task(Task(cli_task, None, None, None, None, None))

    # initialize dict
    for k in settings.tasks:
        occurences_dict[k] = []

    # get files as list
    files = utils.get_files()

    # fill dictionary
    for task in settings.tasks:
        for f in files:
            fill_dictionary(task, f)

    # create list of dict entries and ignore empty task-entries
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
        real_values = []

        for o in occurence_list:
            for line in split_stream(o, task):
                real_values.append(line)

        # find max column widths
        substitutes = [0] * 4 # substitutes for invisible characters
        substitutes[1] = len(BOLD + RESET) # for highlighting tasks # FIXME adjust to new format, individual color per Task?

        if settings.show_paths_for_task_list == args.toggle_paths:
            substitutes[2] = len(BOLD + BLUE + RESET) # for highlighting filename if also showing path
        else:
            substitutes[2] = 0


        max_widths = [0] * 4
        for v in real_values:
            for i in range(len(v)):
                max_widths[i] = max(max_widths[i], len(v[i]))

        if settings.show_paths_for_task_list == args.toggle_paths:
            max_widths[2] -= substitutes[2]

        line_beginning_spacing = "  "
        max_widths[0] = len(line_beginning_spacing)

        # clamp to window width
        s = len(spacing)
        availablespace = int(utils.get_window_size().x) - max_widths[0] - s - max_widths[2] - s - max_widths[3] - s - len(window_padding) + substitutes[1] + s + 6 # the last ' + s + 2' is for setting [0] to 'line_beginning_spacing' and add whitespace to the right side
        max_widths[1] = availablespace

        print(" " + task.color + BOLD + task.representation + " [" + str(len(real_values)) + "]" + RESET)
        print()

        for v in real_values:
            if len(v[1]) > max_widths[1]:
                v[1] = v[1][:max_widths[1]-3] + "..."
            # TODO remove v[0] and max_width[0] because they are not used any more
            # taskword = task.color + v[0].ljust(max_widths[0]) + spacing + RESET # legacy
            taskword = line_beginning_spacing
            line = v[1][:max_widths[1]].ljust(max_widths[1]) + spacing
            filename = v[2].ljust(max_widths[2] + substitutes[2]) + spacing
            linenumber = v[3].rjust(max_widths[3])


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

