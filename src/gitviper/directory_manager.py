import os
from pathlib import Path

GITVIPER_DIRECTORY = Path(__file__).parent.parent  # GitViper root

HOME_DIRECTORY = str(Path.home())
PROJECT_DIRECTORY = str(Path.cwd())

TEMPLATES = f'{GITVIPER_DIRECTORY}/data/templates'
HOME_CONFIG = f"{HOME_DIRECTORY}/.gitviper"
LOCAL_GITVIPER_CONFIG_DIR = f"{PROJECT_DIRECTORY}/.gitviper"  # Relative to cwd (Not GitViper project!)

GIT_HEAD = '.git/HEAD'
MANIFEST = f"{GITVIPER_DIRECTORY}/data/manifest.json"
