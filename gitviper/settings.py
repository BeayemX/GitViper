import gitviper.additional_settings as add_sett

from gitviper.task import Task
from gitviper.colors import *

class Settings:
    def __init__(self):
        self.tasks = []
        self.excluded_directories = [".git"]
        self.excluded_files = []

        self.commit_author_max_length = 20
        self.show_all_categories = False
        self.always_show_authors = False


    def add_task(self, task):
        def get_key(task):
            return task.priority
        self.tasks.append(task)
        self.tasks = sorted(self.tasks, key=get_key, reverse=True)

    def add_excluded_directory(self, new_dir):
        self.excluded_directories.append(new_dir)

    def add_excluded_file(self, new_file):
        self.excluded_files.append(new_file)


# add settings
settings = Settings()

# add tasks
settings.add_task(Task("todo", "Todo", GREEN, BG_GREEN, 5))
settings.add_task(Task("fixme", "FixMe", RED, BG_RED, 10))
settings.add_task(Task("hack", "Hack", YELLOW, BG_YELLOW, 7))

settings.add_task(Task("xxx", "XXX", CYAN, BG_CYAN, 0))

settings.add_task(Task("asdf", "asdf", CYAN, BG_CYAN, 2))
settings.add_task(Task("wip", "WIP", CYAN, BG_CYAN, 4))

# task with a priority below 1 will be displayed in a second line
# settings.add_task(Task("print", "print", BLUE, BG_BLUE, -2))
# settings.add_task(Task("log", "Log", BLUE, BG_BLUE, -1))

# add excluded directories
settings.add_excluded_directory(".git")

# add excluded file
settings.add_excluded_file("settings.py")
settings.add_excluded_file(".sh")
settings.add_excluded_file(".svg")

# load additional settings
add_sett.load_additional_settings(settings)