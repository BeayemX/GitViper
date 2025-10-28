# System
import os
import json
import sys
import time
from shutil import copyfile


# Gitviper
import gitviper

import gitviper.utilities
import gitviper.gitconnector as gitconnector
from gitviper.gitconnector import connection
from gitviper.colors import *

from gitviper.config_loader import get_cli_added_final_config as get_config
from gitviper import directory_manager


# Load configuration
full_path = directory_manager.MANIFEST
with open(full_path) as json_file:
    manifest = json.load(json_file)

## Create constants for configuration values
LABEL = manifest["data"]["label"]
VERSION = manifest["data"]["version"]


# GitViper configuration
final_config_without_cli = get_config(True)
overview_config = final_config_without_cli['overview']


# Custom CLI arguments
def initialize_gitviper_config_files():
    if not os.path.isdir(directory_manager.PROJECT_DIRECTORY + "/.git"):
        arg_string = "--force"
        if (len(sys.argv) > 2 and sys.argv[2] == arg_string) or (len(sys.argv) > 3 and sys.argv[3] == arg_string):
            pass
        else:
            print("This is not a git repository!")
            print("Use " + arg_string + " to force the creation of the .gitviper directory outside of a repository")
            exit()

    if not os.path.isdir(directory_manager.PROJECT_DIRECTORY + "/.gitviper"):
        os.makedirs(directory_manager.PROJECT_DIRECTORY + "/.gitviper")
        print("Initialized GitViper.")
    else:
        arg_string = "--re-init"
        if (len(sys.argv) > 2 and sys.argv[2] == arg_string) or (len(sys.argv) > 3 and sys.argv[3] == arg_string):
            print("Reinitialized GitViper configuration.")
        else:
            print("Configuration folder already exists!")
            print("Use " + arg_string + " to overwrite existing settings.")
            exit()

    # Copy template files
    template_path = directory_manager.TEMPLATES
    local_template_path = directory_manager.LOCAL_GITVIPER_CONFIG_DIR

    for item in os.listdir(template_path):
        copyfile(template_path + "/" + item, local_template_path + "/" + item)
    exit()


if len(sys.argv) > 1:
    if sys.argv[1] == "init":
        initialize_gitviper_config_files()
    else:
        sys_argv_has_been_handled = True

        gitconnector.connect()
        print()

        if sys.argv[1] == "status":
            gitviper.list_status()
        elif sys.argv[1] == "stash":
            gitviper.list_stash()
        elif sys.argv[1] == "log":
            if len(sys.argv) < 3:
                gitviper.list_logs(-1, 0, True)
            else:
                gitviper.list_logs(sys.argv[2], 0, True)
        elif sys.argv[1] == "branch" or sys.argv[1] == "branches":
            gitviper.list_branches(True)
        elif sys.argv[1] == "tasks" or sys.argv[1] == "todo":
            if overview_config['settings']['show_all_tasks']:
                gitviper.list_tasks()

            if overview_config['settings']['show_tasks_for_current_changes'] or overview_config['settings']["show_tasks_for_current_changes_as_bars"]:
                details = overview_config['settings']["show_tasks_for_current_changes"]
                as_bars = overview_config['settings']["show_tasks_for_current_changes_as_bars"]
                gitviper.list_tasks_of_diff(details, as_bars, False)

        else:
            sys_argv_has_been_handled = False

        if sys_argv_has_been_handled:
            print()
            exit()


# Generate label
branch = ""
branch_path = directory_manager.GIT_HEAD
if os.path.isfile(branch_path):
    with open(branch_path, 'r') as myfile:
        branch = myfile.readline().rstrip().rsplit("/")[-1]
        if branch == "master":
            branch = ""


# Execute main program

## Show GitViper label
window_width = gitviper.utilities.get_window_size().x
labeltext = f"{LABEL} {VERSION}-{branch}"
if labeltext[-1] == "-":
    labeltext = labeltext[0 : -1]
labeltext = labeltext.rjust(window_width)
print(labeltext)

## Calculate times
start_time = time.perf_counter()
current_time = start_time

time_separator = "-" * window_width

def show_time():
    global current_time
    delta_time = str(round(time.perf_counter() - current_time, 3))
    print(BOLD + BLUE + (delta_time + " seconds ").rjust(window_width) + RESET)
    reset_time()

def reset_time():
    global current_time
    current_time = time.perf_counter()

def finalize_category(category_is_visible):
    if category_is_visible:
        if overview_config['settings']['show_time'] == True:
            show_time()
            print(BOLD + BLUE + time_separator + RESET)
            print()
        else:
            print()
    else:
        reset_time()


# Load config, now considering command line arguments
final_config = get_config()
overview_config = final_config['overview']

# Main
try:

    # Showing tasks also works for non-git directories
    if overview_config['settings']['show_all_tasks']:
        if overview_config['areas']["tasks"]:
            finalize_category(gitviper.list_tasks())

    # Execute Git related code
    gitconnector.connect()

    if overview_config['settings']['show_tasks_for_current_changes'] or overview_config['settings']["show_tasks_for_current_changes_as_bars"]:
        if overview_config['areas']["tasks"]:
            details = overview_config['settings']["show_tasks_for_current_changes"]
            as_bars = overview_config['settings']["show_tasks_for_current_changes_as_bars"]
            finalize_category(gitviper.list_tasks_of_diff(details, as_bars))

    if connection.is_git_repo:
        if overview_config['areas']["branches"]:
            finalize_category(gitviper.list_branches())
        if overview_config['areas']["logs"]:
            finalize_category(gitviper.list_logs(overview_config['logging']["number"], overview_config['logging']["days"], overview_config['logging']["show_separator"]))
        if overview_config['areas']["stash"]:
            finalize_category(gitviper.list_stash())
        if overview_config['areas']["status"]:
            finalize_category(gitviper.list_status())

except KeyboardInterrupt:
    print()
except BrokenPipeError: # occurs sometimes after quitting less when big git-logs are displayed
    pass

if overview_config['settings']['show_time'] == True:
    current_time = start_time
    show_time()
