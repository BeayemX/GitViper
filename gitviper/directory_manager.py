import os
from pathlib import Path

HOME_DIRECTORY = str(Path.home())
PROJECT_DIRECTORY = os.getcwd()

def get_directories():
    return [HOME_DIRECTORY, PROJECT_DIRECTORY]
