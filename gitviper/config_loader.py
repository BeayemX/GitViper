import os
import json
from pathlib import Path

from gitviper import cli_args_loader
from gitviper import directory_manager

# Configure file directories
GITVIPER_PATH = os.path.dirname(os.path.realpath(__name__))

# Load configuration
full_path = f"{GITVIPER_PATH}/templates/config.json"
with open(full_path) as json_file:
    template_config = json.load(json_file)


def load_config(dir_path):
    full_path = dir_path + "/.gitviper/config.json"

    if os.path.isfile(full_path):
        try:
            with open(full_path) as json_file:
                return json.load(json_file)
        except:
            print(f"Error reading {full_path}")
            pass

    return {}

# Creates a deep copy
def duplicate_config(original_config):
    return json.loads(json.dumps(original_config))

def print_config(cfg):
    print(json.dumps(cfg, indent=2))

def deep_merge_into(original, addition):
    def process_member(source, target):
        for key, value in source.items():
            try:
                target_value = target[key]
            except KeyError:
                continue

            if type(value) == dict:
                process_member(value, target_value)
            else:
                source[key] = target_value

    process_member(original, addition)

def get_startup_config():
    return duplicate_config(template_config)

final_config = None
def get_config():
    global final_config

    if final_config:
        return final_config

    ## Setup value dictionaries
    local_config = load_config(directory_manager.PROJECT_DIRECTORY)
    global_config = load_config(directory_manager.HOME_DIRECTORY)

    final_config = get_startup_config()

    deep_merge_into(final_config, global_config)
    deep_merge_into(final_config, local_config)

    return final_config

def get_cli_added_final_config():
    cli_args, cli_config = cli_args_loader.load_cli_config()

    if cli_args['ignore_config_files']:
        final_config = get_startup_config()
    else:
        final_config = get_config()

    add_cli_config(cli_config, final_config, cli_args)

    if cli_args['debug']:
        print("Final config")
        print_config(final_config)

    return final_config

def add_cli_config(cli_config, final_config, cli_args):
    fin = final_config
    cli = cli_config

    def process_member(parent, source, target):
        for key, value in source.items():
            if isinstance(value, dict):
                process_member(key, value, target[key])
            elif isinstance(value, bool):
                if value:
                    target[key] = not target[key]

                # Will only work if loading cli_config on top
                if parent == 'areas' and cli_args['invert_config_file_values']:
                    target[key] = not target[key]

            elif isinstance(value, int):
                if value > 0:
                    target[key] = value

    process_member(None, cli, fin)