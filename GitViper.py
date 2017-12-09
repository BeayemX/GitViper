import argparse
from pprint import pprint

import gitviper
import gitviper.utilities
import gitviper.gitconnector as gitconnector
from gitviper.gitconnector import connection
from gitviper.colors import *
import time

# module variables
label = "GitViper"
version = "v0.1.2"
branch = "beta"

# command line arguments
# TODO move variables here from settings.py
# e.g. always_show_branches, always_show_author

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--hide-tasks", action='store_true', help="hide the tasks category")
parser.add_argument("-b", "--hide-branches", action='store_true', help="hide the branches category")
parser.add_argument("-s", "--hide-status", action='store_true', help="hide the status category")
parser.add_argument("-st", "--hide-stash", action='store_true', help="hide the stash category")
parser.add_argument("-l", "--hide-logs", action='store_true', help="hide the commit logs category")
parser.add_argument("-ln", "--log-number", type=int, default='5', help="specifiy the number of logs that will be shown")
parser.add_argument("-tm", "--show-time", action='store_true', help="show time needed for each category")

args = parser.parse_args()
#pprint(vars(args))

# main
# print GitViper label
window_width = gitviper.utilities.get_window_size().x
text = label + " " + version + "-" + branch
text = text.rjust(int(window_width))
print(text)

start_time = time.time()

def show_time():
    global start_time
    if args.show_time:
        print("%s seconds" % round(time.time() - start_time, 3))
        start_time = time.time()
        print("-------------------------------------------------------")
        print()


try:
    if not args.hide_tasks:
        gitviper.list_tasks()

    show_time()

    # git
    gitconnector.connect()

    if connection.is_git_repo:
        if not args.hide_branches:
            gitviper.list_branches()
            show_time()
        if not args.hide_logs:
            gitviper.list_logs(args.log_number)
            show_time()
        if not args.hide_stash:
            gitviper.list_stash()
            show_time()
        if not args.hide_status:
            gitviper.list_status()
            show_time()
except KeyboardInterrupt:
    print()
except BrokenPipeError: # occurs sometimes after quitting less when big git-logs are displayed
    pass
