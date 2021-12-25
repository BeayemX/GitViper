import os
from git import Repo
from gitviper.colors import *

class Connection:
    def __init__(self):
        self.repo = None
        self.working_directory = None
        self.is_git_repo = False

connection = Connection()

def connect():
    connection.working_directory = os.getcwd()

    # TODO gitviper should also work if executed in a subdirectory of a git repository
    git_path = os.path.join(connection.working_directory, ".git")

    if os.path.isdir(git_path):
        connection.repo = Repo(connection.working_directory)
        connection.is_git_repo = True
    else:
        print(RED + "This is no git repository!" + RESET)
