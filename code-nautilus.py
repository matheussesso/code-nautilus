# VSCode, Antigravity and Cursor Nautilus Extension
#
# Place me in ~/.local/share/nautilus-python/extensions/,
# ensure you have python-nautilus package, restart Nautilus, and enjoy :)
#
# This script is released to the public domain.

from gi.repository import Nautilus, GObject
from subprocess import call
import os
import json
import shutil

# Editors configuration list
EDITORS = [
    {
        'id': 'VSCode',
        'name': 'VSCode',
        'exec': 'code',
        'tip': 'Opens the selected files with VSCode',
        'tip_bg': 'Opens the current directory in VSCode'
    },
    {
        'id': 'Antigravity',
        'name': 'Antigravity',
        'exec': 'antigravity-ide',
        'tip': 'Opens the selected files with Antigravity IDE',
        'tip_bg': 'Opens the current directory in Antigravity IDE'
    },
    {
        'id': 'Cursor',
        'name': 'Cursor',
        'exec': 'cursor',
        'tip': 'Opens the selected files with Cursor',
        'tip_bg': 'Opens the current directory in Cursor'
    }
]

# Always create new window?
NEW_WINDOW = False


def get_active_editors():
    """
    Returns a list of editors that are enabled in user configuration,
    or falls back to checking if their executables are present in the PATH.
    """
    enabled_ids = None
    config_path = os.path.expanduser('~/.config/code-nautilus/config.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                enabled_ids = config.get('enabled_editors')
        except Exception:
            pass

    active = []
    for editor in EDITORS:
        if enabled_ids is not None:
            if editor['id'] in enabled_ids:
                active.append(editor)
        else:
            # Fallback: only enable if the executable is installed/in PATH
            if shutil.which(editor['exec']):
                active.append(editor)
    return active


class VSCodeExtension(GObject.GObject, Nautilus.MenuProvider):
    """
    Nautilus extension to add 'Open in Code', 'Open in Antigravity',
    and 'Open in Cursor' options to context menus.
    """

    def launch_editor(self, menu, executable, files):
        """
        Launches the specified editor executable with the paths of selected files.
        """
        safepaths = ''
        args = ''

        for file in files:
            filepath = file.get_location().get_path()
            safepaths += '"' + filepath + '" '

            # If one of the files we are trying to open is a folder,
            # create a new instance of the editor.
            if os.path.isdir(filepath) and os.path.exists(filepath):
                args = '--new-window '

        if NEW_WINDOW:
            args = '--new-window '

        call(executable + ' ' + args + safepaths + '&', shell=True)

    def get_file_items(self, *args):
        """
        Returns menu items when one or more files are selected.
        """
        files = args[-1]
        items = []

        for editor in get_active_editors():
            item = Nautilus.MenuItem(
                name=f"{editor['id']}Open",
                label=f"Open in {editor['name']}",
                tip=editor['tip']
            )
            item.connect('activate', self.launch_editor, editor['exec'], files)
            items.append(item)

        return items

    def get_background_items(self, *args):
        """
        Returns menu items when right-clicking the background of a directory.
        """
        file_ = args[-1]
        items = []

        for editor in get_active_editors():
            item = Nautilus.MenuItem(
                name=f"{editor['id']}OpenBackground",
                label=f"Open in {editor['name']}",
                tip=editor['tip_bg']
            )
            item.connect('activate', self.launch_editor, editor['exec'], [file_])
            items.append(item)

        return items
