# GitViper
<img alt="GitViper logo" src="Pictures/GitViperLogo.png" width="256">
GitViper is a tool to improve the experience when using git with the command line by providing you with an overview over the current state of the repository.

## Overview
The overview is split into different categories. Each category is only shown if there is content to be shown.

### Tasks
A task on a keyword you can define. Usually something like `TODO`, `FIXME` or `HACK`. The task category lists the count of all defined keywords throughout the project (directories or filetypes can be excluded).


### Branches
Every remote and every branch on the remote is listed. 
Every local branch is listed, highlights its tracking branch and show how many commits it is ahead and behind.

### Commits
This category shows the last view commits, their commited time and if these commits have differnt authors, also the authors' names.
The header also shows the tracking branch and how many commits can be pushed or pulled. If the current branch does not have a tracking branch it shows an information that it is a local branch.

### Stash
This category shows all stashes, their stash-id and their stash message.

### Status
The status category shows all staged, unstaged and untracked files. Each subcategory will only be display if there are files that belong to that subcategory.

![GitViper overview](Pictures/GitViperOverview.png)

## Task list
The task list is used to show every task (that has been defined) and where it occurs. It shows the line content, the file name and the line number.
![GitViper task list](Pictures/GitViperTodo.png)


## Installation
GitViper uses **GitPython** for working with the git repository and the **humanize** package to display times and dates in a more readable way.

Both can be installed using

`pip3 install GitPython`

`pip3 install humanize`

Alternativly the humanize package can be installed with 

`sudo apt-get install python3-humanize` 

on Linux Mint or something similar on other distros.
