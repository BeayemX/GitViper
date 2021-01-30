<p align="center">
    <img src="https://user-images.githubusercontent.com/3453076/35360877-8035c5b2-015f-11e8-8ab2-1d74e65e3cd5.png" alt="GitViper logo">
</p>

# GitViper
GitViper is a tool to improve the experience when using Git with the command line by showing you the current state of the repository. This tool is designed to only display git related information. You can still work with Git and modify files the way you want.

## Installation
GitViper builds on top of Git, therefore it is required to have Git installed on your system. Just use your package manager to install Git. The command should look something along these lines:
```
sudo apt-get install git
sudo dnf install git
```

GitViper uses **[GitPython](https://github.com/gitpython-developers/GitPython)** for working with the git repository and the **[humanize](https://github.com/jmoiron/humanize)** package to display times and dates in a more readable way.

All dependencies can be installed using the provided `requirements.txt` by running

```
pip3 install -r requirements.txt
```

which needs:

```
sudo apt install python3-pip
```

Alternativly the humanize package can be installed with

```
sudo apt-get install python3-humanize
```

on Linux Mint or something similar on other distros.

## How to use GitViper
There are two python files you can use. `GitViper.py` is used to display the mainview for the current repository. Your current working directory has to be the root level of a git repository. Individual sections can also be display solely. You can see every command in the according section.

The second file is `TaskList.py` which is used to list all occurences of task-keywords.

For convenience's sake there is also `GitViperLoader.sh` which can be used to add aliases for these two files to your bash environment by running

```
source ~/GitViper/GitViperLoader.sh
```

or putting this line into your `.bashrc`. Just make sure you are using the right directory. It also adds some more shortcuts to improve the overall experience. For example if you use this convencience-file aliases all commands clear the screen before showing information. If you just want to use the python files you can still take a look inside this file to see possible calls with different command line arguments. or you can show the help by executing:

```
gitviper --help
```

## Main view

![image](https://user-images.githubusercontent.com/3453076/35360910-9935f38e-015f-11e8-9b4f-447c99c8a92a.png)

The main view is split into different categories. Each category is only shown if there is content to be shown. You can also disable specific categories by passing arguments to GitViper. To see a list of available options use `gitviper --help`.

**Tasks**

```
gitviper task
```

or

```
gitviper tasks
```

A task is a keyword you can define. Usually something like `TODO`, `FIXME` or `HACK`. The task category lists the count of all defined keywords throughout the project (directories or filetypes can be excluded). You can adjust these keywords in the `/.gitviper/tasks` file and add priorities to different tasks. For further information regarding configuration see the Configuration section. The tasks will be sorted descending by their priority.

**Branches**

```
gitviper branch
```

or

```
gitviper branches
```

Every remote and every branch on the remote is listed.
Every local branch is listed, highlights its tracking branch and shows how many commits it is ahead and behind.

**Commits**

```
gitviper log
```

This category shows the last few commits, their committed time and if these commits have different authors, also the authors' names. The first word of each commit message is also highlighted to make it easier to identify each commit's purpose.
The header also shows the tracking branch and how many commits can be pushed or pulled. If the current branch does not have a tracking branch it shows a hint that it is a local branch.

**Stash**

```
gitviper stash
```

This category shows all stashes, their stash-IDs and their stash messages.

**Status**

```
gitviper status
```

The status category shows all staged, unstaged and untracked files. Each subcategory will only be display if there are files that belong to that subcategory.

## Task list

![untitled](https://user-images.githubusercontent.com/3453076/48317511-b6b61500-e5f3-11e8-8426-5bee86120cc0.png)

You can display the task list by running the `TaskList.py` file or if you are using the `GitViperLoader.sh` file by running `todo`. The task list is used to show every task (that has been defined in the `.gitviper/tasks` file) and where it occurs. It shows the line content, the path and the line number.

There are several optional options available.
A task looks something like this

```
[To-Do]
key = todo
color = yellow
bold = true
font color = black
row = 0
priority = 1
# disabled
```

All lines except for the section header are optional. If one line is not used it will fallback to a default value. The `disabled` setting can be used to ignore globally defined tasks.

If you want to show additional task-keywords in the TaskList you can use an arbitrary number of keywords when using the `-a` flag.
Example usage:

```
tasklist -a myNewTask anotherTask
```

The configuration can be ignored by using `-i`. This is useful if only undefined Tasks should be displayed. eg 

```
tasklist -i -a onlyShowThisTask andThisTask
```

## Configuration
Many things that are displayed can be adjusted in the configuration files. You can configure tasks, ignored files / directories and default values for the standard `GitViper` display.
These settings are split into several files and can be seen in the templates directory.

To create a local directory with all files use `gitviper init`. 
This will copy the files located in `templates` into a `.gitviper` folder. The templates include comments and show all possible values that can be used. If you want to change values which will be used for every initialzation just adjust the files in the template directory accordingly.

You can also use a `.gitviper` directory in your home directory to use these configurations for every repository. The values from this global configuration will be overwritten by a local configuration.

It is also possible to ignore all configurations. This is usefull if you are checking multiple different repositores, so you don't have to know every repository specific configuration. If you want to see the last few commits in each repository you can just use

```
gitviper --ignore-conf -l -inv -ln 10
```

and you don't have to worry about global or local configurations.


## Feedback and bugs
If you encounter bugs or want to request new features just open an issue.
