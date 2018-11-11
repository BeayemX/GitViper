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


from pathlib import Path
import os

home_dir = str(Path.home())
project_dir = os.getcwd()
directories = [home_dir, project_dir]
gitviper_path = os.path.dirname(os.path.realpath(__file__))


import sys
if len(sys.argv) > 1:
    if sys.argv[1] == "init":
        if not os.path.isdir(project_dir + "/.git"):
            print("This is not a git repository!")
            exit()

        if not os.path.isdir(project_dir + "/.gitviper"):
            os.makedirs(project_dir + "/.gitviper")
            print("Initialized GitViper.")
        else:
            print("Reinitialized GitViper.")

        # copy template files
        from shutil import copyfile
        template_path = gitviper_path + "/templates"
        local_template_path = project_dir + "/.gitviper"

        for item in os.listdir(template_path):
            copyfile(template_path + "/" + item, local_template_path + "/" + item)
        exit()

    else:
        sys_argv_has_been_handled = True

        gitconnector.connect()
        if sys.argv[1] == "status":
            print()
            gitviper.list_status()
        elif sys.argv[1] == "stash":
            print()
            gitviper.list_stash()
        elif sys.argv[1] == "log":
            print()
            if len(sys.argv) < 3:
                gitviper.list_logs(-1, 0, True)
            else:
                gitviper.list_logs(sys.argv[2], 0, True)
        elif sys.argv[1] == "branch" or sys.argv[1] == "branches":
            print()
            gitviper.list_branches(True)
        elif sys.argv[1] == "tasks" or sys.argv[1] == "todo":
            print()
            gitviper.list_tasks()
        else:
            sys_argv_has_been_handled = False

        if sys_argv_has_been_handled:
            print()
            exit()

# module variables
label = "GitViper"
version = "v0.2"
branch = ""
branch_path = gitviper_path + '/.git/HEAD'
if os.path.isfile(branch_path):
    with open(branch_path, 'r') as myfile:
        branch = myfile.readline().rstrip().rsplit("/")[-1]
        if branch == "master":
            branch = ""


# load default values for cli arguments
default_values = {
    "ignore_conf" : False,
    "tasks" : True,
    "branches" : True,
    "status" : True,
    "stash" : True,
    "logs" : True,
    "time" : False,
    "separate_commits" : False,
    "log_number" : 5,
    "max_days" : 0,
    "invert": False
}

# setup value dictionaries
cli_arg_values = {}
conf_values = {}
final_values = {}

for key in default_values:
    cli_arg_values[key] = None
    conf_values[key] = None
    final_values[key] = default_values[key]


def load_defaults(dir_path):
    full_path = dir_path + "/.gitviper/config"

    if not os.path.isfile(full_path):
        return

    config = configparser.ConfigParser()
    config.read(full_path)
    try:
        conf_values["tasks"] = config["Display Settings"].getboolean("show-tasks")
        conf_values["branches"] = config["Display Settings"].getboolean("show-branches")
        conf_values["status"] = config["Display Settings"].getboolean("show-status")
        conf_values["stash"] = config["Display Settings"].getboolean("show-stash")
        conf_values["logs"] = config["Display Settings"].getboolean("show-logs")
        conf_values["time"] = config["Display Settings"].getboolean("show-time")
    except KeyError:
        pass

    try:
        conf_values["separate_commits"] = config["Log Settings"].getboolean("show-separator")
        conf_values["log_number"] = config["Log Settings"].getint("log-number")
        conf_values["max_days"] = config["Log Settings"].getint("log-days")
    except KeyError:
        pass


for directory in directories:
    load_defaults(directory)

# command line arguments
parser = argparse.ArgumentParser(description="This will show all values that can be toggled. The initial value is gathered from the configuration file(s). The default values are used if there are no files provided.")
parser.add_argument("-ig", "--ignore-conf", action="store_true", help="ignore all configuration files and use the default values")
parser.add_argument("-t", "--tasks", action="store_true", help="toggle the tasks category")
parser.add_argument("-b", "--branches", action="store_true", help="toggle the branches category")
parser.add_argument("-s", "--status", action="store_true", help="toggle the status category")
parser.add_argument("-st", "--stash", action="store_true", help="toggle the stash category")
parser.add_argument("-l", "--logs", action="store_true", help="toggle the commit logs category")
parser.add_argument("-ln", "--log-number", type=int, default=0, help="specifiy the number of logs that will be shown")
parser.add_argument("-tm", "--time", action="store_true", help="show time needed for each category")
parser.add_argument("-d", "--max-days-old", type=int, default=0, help="specifiy the number of days to consider for the commit log")
parser.add_argument("-sep", "--separate-commits", action="store_true", help="separate the commit logs by days")
parser.add_argument("--debug", action="store_true", help="show debug logs")

parser.add_argument("-inv", "--invert", action='store_true', help="invert the given values")

args = parser.parse_args()

# cli toggles
cli_arg_values["ignore_conf"] = args.ignore_conf
cli_arg_values["tasks"] = args.tasks
cli_arg_values["branches"] = args.branches
cli_arg_values["status"] = args.status
cli_arg_values["stash"] = args.stash
cli_arg_values["logs"] = args.logs
cli_arg_values["time"] = args.time
cli_arg_values["separate_commits"] = args.separate_commits
cli_arg_values["invert"] = args.invert

# cli values
cli_arg_values["max_days"] = args.max_days_old
cli_arg_values["log_number"] = args.log_number

# overwrite values with config values
if cli_arg_values["ignore_conf"] == False:
    for key in conf_values:
        if conf_values[key] != None:
            final_values[key] = conf_values[key] # do i have to init final_ with default values? because conf_ will also have default values if not set, right?

# command line args to flip value
for key in cli_arg_values:
    if isinstance(final_values[key], bool):
        if cli_arg_values[key] == True:
            final_values[key] = not final_values[key]
    elif int(cli_arg_values[key]) > 0:
        final_values[key] = int(cli_arg_values[key])


# # # print values
if args.debug:
    print("key".ljust(16), "default", "cli-ar", "conf", "final", sep="\t")
    print()
    for key in default_values:
        print(key.ljust(16), default_values[key], cli_arg_values[key], conf_values[key], final_values[key], sep="\t")




# Execute main program

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
        if final_values["time"] == True:
            show_time()
            print(BOLD + BLUE + time_separator + RESET)
            print()
        else:
            print()
    else:
        reset_time()

try:
    if final_values["tasks"] != final_values["invert"]:
        finalize_category(gitviper.list_tasks())

    # git
    gitconnector.connect()

    if connection.is_git_repo:
        if final_values["branches"] != final_values["invert"]:
            finalize_category(gitviper.list_branches())
        if final_values["logs"] != final_values["invert"]:
            finalize_category(gitviper.list_logs(final_values["log_number"], final_values["max_days"], final_values["separate_commits"]))
        if final_values["stash"] != final_values["invert"]:
            finalize_category(gitviper.list_stash())
        if final_values["status"] != final_values["invert"]:
            finalize_category(gitviper.list_status())

except KeyboardInterrupt:
    print()
except BrokenPipeError: # occurs sometimes after quitting less when big git-logs are displayed
    pass

if final_values["time"] == True:
    current_time = start_time
    show_time()
