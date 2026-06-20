# VSCode and Antigravity Nautilus Extension
#
# Place me in ~/.local/share/nautilus-python/extensions/,
# ensure you have python-nautilus package, restart Nautilus, and enjoy :)
#
# This script is released to the public domain.

from gi.repository import Nautilus, GObject
from subprocess import call
import os

# Paths to the executables
VSCODE = 'code'
ANTIGRAVITY = 'antigravity-ide'

# Names for the context menu items
VSCODE_NAME = 'Code'
ANTIGRAVITY_NAME = 'Antigravity'

# Always create new window?
NEW_WINDOW = False


class VSCodeExtension(GObject.GObject, Nautilus.MenuProvider):
    """
    Nautilus extension to add 'Open in Code' and 'Open in Antigravity'
    options to context menus.
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

        vscode_item = Nautilus.MenuItem(
            name='VSCodeOpen',
            label='Open in ' + VSCODE_NAME,
            tip='Opens the selected files with VSCode'
        )
        vscode_item.connect('activate', self.launch_editor, VSCODE, files)

        antigravity_item = Nautilus.MenuItem(
            name='AntigravityOpen',
            label='Open in ' + ANTIGRAVITY_NAME,
            tip='Opens the selected files with Antigravity IDE'
        )
        antigravity_item.connect('activate', self.launch_editor, ANTIGRAVITY, files)

        return [vscode_item, antigravity_item]

    def get_background_items(self, *args):
        """
        Returns menu items when right-clicking the background of a directory.
        """
        file_ = args[-1]

        vscode_item = Nautilus.MenuItem(
            name='VSCodeOpenBackground',
            label='Open in ' + VSCODE_NAME,
            tip='Opens the current directory in VSCode'
        )
        vscode_item.connect('activate', self.launch_editor, VSCODE, [file_])

        antigravity_item = Nautilus.MenuItem(
            name='AntigravityOpenBackground',
            label='Open in ' + ANTIGRAVITY_NAME,
            tip='Opens the current directory in Antigravity IDE'
        )
        antigravity_item.connect('activate', self.launch_editor, ANTIGRAVITY, [file_])

        return [vscode_item, antigravity_item]

