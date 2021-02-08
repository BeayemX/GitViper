import os.path
import json

from gitviper.task import Task
from gitviper.colors import *

from gitviper import directory_manager
from gitviper.config_loader import get_config


class TaskLoader:
    def __init__(self):
        self.tasks = []
        self.ignored_directories = []
        self.ignored_files = []

        self.strip_comment_symbols = True
        self.show_paths_for_task_list = True
        self.show_tasks_only_for_current_changes = True

    def add_task(self, task):
        def get_key(task):
            return task.priority

        # TODO use dict to be able to directly access task with similar representation?
        # would avoid iterating over all tasks
        self.remove_task(task.representation)

        self.tasks.append(task)
        self.tasks = sorted(self.tasks, key=get_key, reverse=True)

    def remove_task(self, task_representation):
        for task_entry in self.tasks:
            if task_entry.representation == task_representation:
                self.tasks.remove(task_entry)
                return

    def clear_tasks(self):
        self.tasks = [] # will not update references made to 'task_loader.tasks'

    def add_ignored_directory(self, new_dir):
        self.ignored_directories.append(new_dir)

    def add_ignored_file(self, new_file):
        self.ignored_files.append(new_file)


def _call_function_with_every_line_in_file(function, dir_path, file_name):
    full_path = dir_path + file_name

    if not os.path.isfile(full_path):
        return

    with open(full_path) as file:
        for line in file:
            line = line.rstrip('\n')
            if line != '':
                function(line)


def _load_ignored_files(dir_path):
    _call_function_with_every_line_in_file(task_loader.add_ignored_file, dir_path, "ignored_files")


def _load_ignored_directories(dir_path):
    _call_function_with_every_line_in_file(task_loader.add_ignored_directory, dir_path, "ignored_directories")


# Load additional task_loader
def _load_tasks_from_config_file(dir_path):
    full_path = dir_path + "/tasks.json"

    if not os.path.isfile(full_path):
        return

    try:
        with open(full_path, 'r') as f:
            config = json.load(f)
    except json.decoder.JSONDecodeError:
        print(f"JSON at '{full_path}' is corrupted!")
        return

    for task_name, task_obj in config.items():
        if task_obj.get("disabled") == True:  # Can be used to override global tasks to avoid for specific projects
            task_loader.remove_task(task_name)
        else:
            task_loader.add_task(Task(task_name, task_obj))

# Actual execution
task_loader = TaskLoader()

# This will load all configured tasks (global and local)
directories = directory_manager.get_directories()

for directory in directories:
    _load_tasks_from_config_file(directory)
    _load_ignored_directories(directory)
    _load_ignored_files(directory)
