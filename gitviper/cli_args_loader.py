import argparse

def load_cli_config():
    # Command line arguments
    ## Modify settings
    parser = argparse.ArgumentParser(description="This will show all values that can be toggled. The initial value is gathered from the configuration file(s). The default values are used if there are no files provided.")
    parser.add_argument("-t", "--tasks", action="store_true", help="toggle the tasks category")
    parser.add_argument("-td", "--tasks-diff", action="store_true", help="toggle tasks showing only for the currently modified files or all files")
    parser.add_argument("-tl", "--list-tasks-diff", action="store_true", help="toggle listing task occurences for the currently modified files or all files")
    parser.add_argument("-b", "--branches", action="store_true", help="toggle the branches category")
    parser.add_argument("-s", "--status", action="store_true", help="toggle the status category")
    parser.add_argument("-st", "--stash", action="store_true", help="toggle the stash category")
    parser.add_argument("-l", "--logs", action="store_true", help="toggle the commit logs category")
    parser.add_argument("-ln", "--log-number", type=int, default=0, help="specifiy the number of logs that will be shown")
    parser.add_argument("-tm", "--time", action="store_true", help="show time needed for each category")
    parser.add_argument("-d", "--max-days-old", type=int, default=0, help="specifiy the number of days to consider for the commit log")
    parser.add_argument("-sep", "--separate-commits", action="store_true", help="separate the commit logs by days")

    ## Change config file behaviour
    parser.add_argument("-ig", "--ignore-conf", action="store_true", help="ignore all configuration files and use the default values")
    parser.add_argument("-inv", "--invert", action='store_true', help="invert the visibiltiy of the configured areas")

    ## Other settings
    parser.add_argument("--debug", action="store_true", help="show debug logs")

    args = parser.parse_args()

    ## cli toggles
    cli_args = {
        'ignore_config_files': args.ignore_conf,
        'invert_config_file_values': args.invert,
        'debug': args.debug
    }

    # FIXME Is there a better way to make sure that merging is possible, besides manually creating the same structure?
    cli_conf = {
        "overview":{
            "areas": {
                "tasks": args.tasks,
                "branches": args.branches,
                "logs": args.logs,
                "stash": args.stash,
                "status": args.status
            },
            "settings": {
                "show_time": args.time,
                "show_tasks_only_for_current_changes": args.tasks_diff,
                "show_task_lines_in_overview": args.list_tasks_diff
            },
            "logging": {
                "number": args.log_number,
                "days": args.max_days_old,
                "show_separator": args.separate_commits
            }
        }
    }

    return cli_args, cli_conf