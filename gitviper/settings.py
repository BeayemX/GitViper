import os.path
import configparser

from gitviper.task import Task
from gitviper.colors import *

class Settings:
    def __init__(self):
        self.tasks = []
        self.ignored_directories = []
        self.ignored_files = []

        self.commit_author_max_length = 0
        self.always_show_authors = True

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
        self.tasks = [] # will not update references made to 'settings.tasks'

    def add_ignored_directory(self, new_dir):
        self.ignored_directories.append(new_dir)

    def add_ignored_file(self, new_file):
        self.ignored_files.append(new_file)


def _call_function_with_every_line_in_file(function, dir_path, file_name):
    full_path = dir_path + "/.gitviper/" + file_name
    if not os.path.isfile(full_path):
        return

    with open(full_path) as file:
        for line in file:
            line = line.rstrip('\n')
            if line != '':
                function(line)

def _load_ignored_files(dir_path):
    _call_function_with_every_line_in_file(settings.add_ignored_file, dir_path, "ignored_files")

def _load_ignored_directories(dir_path):
    _call_function_with_every_line_in_file(settings.add_ignored_directory, dir_path, "ignored_directories")

# load additional settings
def _load_tasks_from_config_file(dir_path):
    full_path = dir_path + "/.gitviper/tasks"

    if not os.path.isfile(full_path):
        return

    config = configparser.ConfigParser(allow_no_value = True)
    config.read(full_path)

    for section in config.sections():
        sec = config[section]
        try:
            sec["disabled"] # can be used to override global tasks to avoid for specific projects
        except KeyError: # HACK using expected exception for logical flow!?!
            settings.add_task(Task(
                section,
                sec.get("key"),
                sec.get("color"),
                sec.getint("priority"),
                sec.get("font color"),
                sec.getboolean("bold"),
                sec.getint("row")
            ))
        else:
            settings.remove_task(section)

def _load_settings(dir_path):
    full_path = dir_path + "/.gitviper/config"

    if not os.path.isfile(full_path):
        return

    config = configparser.ConfigParser()
    config.read(full_path)

    # Commit Log Settings
    try:
        log_section = config["Log Settings"]
    except KeyError:
        pass
    else:
        val = log_section.getboolean("always-show-author")
        if val != None:
            settings.always_show_authors =  val

        val = log_section.getint("commit-author-max-length")
        if val:
            settings.commit_author_max_length = val

    # Task View Settings
    try:
        task_view_section = config["Task View"]
    except KeyError:
        pass
    else:
        val = task_view_section.getboolean("show-path")
        if val != None:
            settings.show_paths_for_task_list = val

        val = task_view_section.getboolean("strip-comment-symbols")
        if val != None:
            settings.strip_comment_symbols = val


# actual execution
settings = Settings()

from pathlib import Path
home_dir = str(Path.home())
project_dir = os.getcwd()
directories = [home_dir, project_dir]

for directory in directories:
    _load_settings(directory)
    _load_tasks_from_config_file(directory)
    _load_ignored_directories(directory)
    _load_ignored_files(directory)
