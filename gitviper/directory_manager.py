import os
from pathlib import Path

root_path = None

ROOT_DIR = Path(__file__).parent.parent

HOME_DIRECTORY = str(Path.home())
PROJECT_DIRECTORY = os.getcwd()

def get_directories():
    return [
        f"{ROOT_DIR}/templates",
        f"{HOME_DIRECTORY}/.gitviper",
        f"{PROJECT_DIRECTORY}/.gitviper",
    ]

def set_root_path(path):
    global root_path
    root_path = path

def get_root_path():
    return root_path