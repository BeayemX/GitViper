from gitviper.colors import *

class Task:
    def __init__(self, value, representation=None, color=None, bgcolor=None, priority=0):
        self.value = value
        self.representation = representation
        self.color = color
        self.bgcolor = bgcolor
        self.priority = priority

class Settings:
    def __init__(self):
        self.tasks = []
        self.excluded_directories = set([".git"])
        self.excluded_files = set(["settings.py", ".sh", ".svg"])

        self.commit_author_max_length = 20
        self.show_all_categories = False
        self.always_show_authors = False


    def add_task(self, task):
        def get_key(task):
            return task.priority
        self.tasks.append(task)
        self.tasks = sorted(self.tasks, key=get_key, reverse=True)


settings = Settings()

settings.add_task(Task("todo", "Todo", GREEN, BG_GREEN, 5))
settings.add_task(Task("fixme", "FixMe", RED, BG_RED, 10))
settings.add_task(Task("hack", "Hack", YELLOW, BG_YELLOW, 7))

settings.add_task(Task("xxx", "XXX", CYAN, BG_CYAN, 0))

settings.add_task(Task("asdf", "asdf", CYAN, BG_CYAN, 2))
settings.add_task(Task("wip", "WIP", CYAN, BG_CYAN, 4))

# task with a priority below 1 will be displayed in a second line
# settings.add_task(Task("print", "print", BLUE, BG_BLUE, -2))
# settings.add_task(Task("log", "Log", BLUE, BG_BLUE, -1))
