import os
import argparse
import configparser
from pprint import pprint

import gitviper
import gitviper.utilities
import gitviper.gitconnector as gitconnector
from gitviper.gitconnector import connection
from gitviper.colors import *
import time

# module variables
label = "GitViper"
version = "v0.1.6"
branch = ""

path = os.path.dirname(os.path.realpath(__file__))
with open(path + '/.git/HEAD', 'r') as myfile:
    branch = myfile.readline().rstrip().rsplit("/")[-1]
    if branch == "master":
        branch = ""


# load default values for cli arguments
default_values = {
    "show_everything" : False,
    "tasks" : False,
    "branches" : False, # TODO should be auto
    "status" : True,
    "stash" : True,
    "logs" : True,
    "time" : False,
    "separate_commits" : False,
    "line_number" : 5,
    "max_days" : 0
}

def load_defaults(dir_path):
    full_path = dir_path + "/.gitviper/config"

    if not os.path.isfile(full_path):
        return

    config = configparser.ConfigParser()
    config.read(full_path)

    def get_value(default_value, section, var_name):
        default_value = default_values[default_value]
        try:
            conf_value = config[section][var_name]
        except KeyError:
            return default_value

        # FIXME duplicate call because try block is other scope...
        conf_value = config[section][var_name]
        if conf_value == None:
            return default_value
        else:
            return conf_value

    default_values["show_everything"] = get_value("show_everything", "Display Settings", "show-everything")
    default_values["tasks"] = get_value("tasks", "Display Settings", "show-tasks")
    default_values["branches"] = get_value("branches", "Display Settings", "show-branches")
    default_values["status"] = get_value("status", "Display Settings", "show-status")
    default_values["stash"] = get_value("stash", "Display Settings", "show-stash")
    default_values["logs"] = get_value("logs", "Display Settings", "show-logs")
    default_values["time"] = get_value("time", "Display Settings", "show-time")
    default_values["separate_commits"] = get_value("separate_commits", "Log Settings", "show-separator")

    default_values["line_number"] = get_value("line_number", "Log Settings", "log-number") # int
    default_values["max_days"] = get_value("max_days", "Log Settings", "log-days") # int

def action(arg, flip = None): # HACK 'flip' should not be required, somtimes it is there because previously it was 'store_false'?
    def_val = default_values[arg]
    def_val = str(def_val).lower()
    if (def_val == "true") != (flip != None):
        return "store_true"
    if (def_val == "false") != (flip != None):
        return "store_false"
    return def_val

from pathlib import Path
import os
home_dir = str(Path.home())
project_dir = os.getcwd()
directories = [home_dir, project_dir]

for directory in directories:
    load_defaults(directory)

# command line arguments
# TODO move variables here from settings.py
# e.g. always_show_branches, always_show_author

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--hide-tasks", action=action("tasks"), help="hide the tasks category")
parser.add_argument("-b", "--hide-branches", action=action("branches"), help="hide the branches category")
parser.add_argument("-s", "--hide-status", action=action("status"), help="hide the status category")
parser.add_argument("-st", "--hide-stash", action=action("stash"), help="hide the stash category")
parser.add_argument("-l", "--hide-logs", action=action("logs"), help="hide the commit logs category")
parser.add_argument("-ln", "--log-number", type=int, default=default_values["line_number"], help="specifiy the number of logs that will be shown")
parser.add_argument("-tm", "--show-time", action=action("time", "flip"), help="show time needed for each category")
parser.add_argument("-d", "--max-days-old", type=int, default=default_values["max_days"], help="specifiy the number of days to consider for the commit log")
parser.add_argument("-sep", "--separate-commits", action=action("separate_commits", "flip"), help="separate the commit logs by days")

# only cli args, not in the config file
parser.add_argument("-inv", "--show-only", action='store_true', help="only show the given categories instead of hiding them")
# TODO add --ignore-config-file

args = parser.parse_args()
#pprint(vars(args))

# main
# print GitViper label
window_width = gitviper.utilities.get_window_size().x
text = label + " " + version + "-" + branch
if text[-1] == "-":
    text = text[0 : -1]
text = text.rjust(int(window_width))
print(text)

start_time = time.time()
current_time = start_time

time_separator = "".join(["-"] * int(window_width))

def show_time():
    global current_time
    delta_time = str(round(time.time() - current_time, 3))
    print(BOLD + BLUE + (delta_time + " seconds ").rjust(int(window_width)) + RESET)
    reset_time()

def reset_time():
    global current_time
    current_time = time.time()

def finalize_category(category_is_visible):
    if category_is_visible:
        if args.show_time:
            show_time()
            print(BOLD + BLUE + time_separator + RESET)
            print()
        else:
            print()
    else:
        reset_time()

try:
    if args.hide_tasks == args.show_only:
        finalize_category(gitviper.list_tasks())

    # git
    gitconnector.connect()

    if connection.is_git_repo:
        if args.hide_branches == args.show_only:
            finalize_category(gitviper.list_branches())
        if args.hide_logs == args.show_only:
            finalize_category(gitviper.list_logs(args.log_number, args.max_days_old, args.separate_commits))
        if args.hide_stash == args.show_only:
            finalize_category(gitviper.list_stash())
        if args.hide_status == args.show_only:
            finalize_category(gitviper.list_status())

except KeyboardInterrupt:
    print()
except BrokenPipeError: # occurs sometimes after quitting less when big git-logs are displayed
    pass

if args.show_time:
    current_time = start_time
    show_time()
