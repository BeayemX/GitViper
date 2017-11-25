<img alt="GitViper logo" src="Pictures/GitViperLogo.png" width="256">

# GitViper
GitViper is a tool to improve the experience when using Git with the command line by showing you the current state of the repository. This tool is designed to only display git related information. You can still work with Git and modify files the way you want.

## How to use GitViper
To be able to use GitViper you just have to load the `GitViperLoader.sh` file into your bash (i.e. `source ~/GitViper/GitViperLoader.sh`). This file adds aliases for both python scripts (`GitViper.py` and `TaskList.py`) to your bash environment. It also adds shortcuts to some Git commands to bypass the `git ` prefix needed to execute the command and also to clear the screen before the execution and showing the GitViper main view afterwards. If you want to modify the aliases or see possible GitViper calls, take a look at this file. To see all possible command line arguments use 
```
gitviper --help
```

## Main view
![GitViper overview](Pictures/GitViperOverview.png)

The main view is split into different categories. Each category is only shown if there is content to be shown. You can also disable specific categories by passing arguments to GitViper.

**Tasks**

A task is a keyword you can define. Usually something like `TODO`, `FIXME` or `HACK`. The task category lists the count of all defined keywords throughout the project (directories or filetypes can be excluded).


**Branches**

Every remote and every branch on the remote is listed. 
Every local branch is listed, highlights its tracking branch and shows how many commits it is ahead and behind.

**Commits**

This category shows the last few commits, their committed time and if these commits have different authors, also the authors' names.
The header also shows the tracking branch and how many commits can be pushed or pulled. If the current branch does not have a tracking branch it shows a hint that it is a local branch.

**Stash**

This category shows all stashes, their stash-IDs and their stash messages.

**Status**

The status category shows all staged, unstaged and untracked files. Each subcategory will only be display if there are files that belong to that subcategory.

## Task list
![GitViper task list](Pictures/GitViperTodo.png)

The task list is used to show every task (that has been defined in the settings) and where it occurs. It shows the line content, the file name and the line number.


## Installation
GitViper uses **GitPython** for working with the git repository and the **humanize** package to display times and dates in a more readable way.

Both can be installed using

```
pip3 install GitPython
pip3 install humanize
```

Alternativly the humanize package can be installed with 

```
sudo apt-get install python3-humanize
```

on Linux Mint or something similar on other distros.
