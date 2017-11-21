from pprint import pprint

import gitviper.gui as gui
import gitviper.gitstuff as gitstuff

from gitviper.colors import *
from gitviper.gitconnector import connection
from gitviper.settings import settings

spacing = "  "
branches_indentation = "   "

def list_branches():
    if should_show_branches():
        gui.print_header("Branches", BG_MAGENTA)

        try:
            refs = connection.repo.remotes.origin.refs
        except AttributeError:
            _list_local_branches()
        else:
            _list_all_branches()

        print()

def should_show_branches():
    remotes = connection.repo.remotes

    if len(remotes) > 1:
        return True

    for remote in remotes:
        if len(remote.refs) > 1:
            return True

    return settings.show_all_categories

def _list_all_branches():
    _list_remote_branches()
    _list_local_branches()

def _list_remote_branches():
    remotes = connection.repo.remotes

    for remote in remotes:
        refs = remote.refs
        print(WHITE + BOLD + " " + remote.name + " " + RESET + "(" + str(len(refs)) + ")")

        text = "   "
        trackingbranchname = ""

        if connection.repo.active_branch.tracking_branch() != None:
            trackingbranchname = connection.repo.active_branch.tracking_branch().name

        for branch in refs:
            if trackingbranchname == branch.name:
                text += GREEN

            text += branch.name
            text += spacing

            text += RESET

        print(text)

def _list_local_branches():
    branches = connection.repo.branches
    print(WHITE + BOLD + " local " + RESET + "(" + str(len(branches)) + ")")

    text = branches_indentation

    for branch in branches:
        color = ""
        ahead = gitstuff.get_ahead(branch)
        behind = gitstuff.get_behind(branch)

        if gitstuff.remote_exists(branch):
            color = ""

            if branch.name == connection.repo.active_branch.name:
                color = GREEN

            text += color
            text += branch.name

            if ahead > 0 or behind > 0:
                text += "(" + str(ahead) + "|" + str(behind) + ")"

            text += spacing
            text += RESET

        else: # local-only branch
            if branch.name == connection.repo.active_branch.name:
                text+= GREEN

            text += "<" + branch.name + ">" + spacing + RESET
            text += RESET

    print(text)
