import os
from pathlib import Path

root_path = None

HOME_DIRECTORY = str(Path.home())
PROJECT_DIRECTORY = os.getcwd()

def get_directories():
    return [HOME_DIRECTORY, PROJECT_DIRECTORY]

def set_root_path(path):
    global root_path
    root_path = path

def get_root_path():
    return root_path