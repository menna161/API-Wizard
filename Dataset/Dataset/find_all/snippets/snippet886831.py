import os
import sys
import logging
from wcwidth import wcswidth
from .prompt import Prompt, PromptBool, PromptFiltered, PromptFile, PromptAutocmp
from .key_mappings import key_map
import curses
import pygments


def show_legend(self):
    'Show keyboard legend.'
    legend_commands = [('save_file', 'Save'), ('save_file_as', 'Save as'), ('reload_file', 'Reload'), ('undo', 'Undo'), ('redo', 'Redo'), ('open', 'Open'), ('copy', 'Copy'), ('cut', 'Cut'), ('insert', 'Paste'), ('find', 'Find'), ('find_next', 'Find next'), ('find_all', 'Find all'), ('duplicate_line', 'Duplicate line'), ('escape', 'Single cursor'), ('go_to', 'Go to'), ('run_command', 'Run command'), ('toggle_mouse', 'Mouse mode'), ('help', 'Help'), ('ask_exit', 'Exit')]
    keys = []
    for command in legend_commands:
        for item in self.app.config.keymap:
            if (item['command'] == command[0]):
                key = item['keys'][0]
                keys.append((key, command[1]))
                break
    self.legend_win.erase()
    x = 0
    y = 0
    max_y = 1
    for item in keys:
        key = item[0]
        label = item[1]
        key = key.upper()
        if key.startswith('CTRL+'):
            key = ('^' + key[5:])
        if (key == 'ESCAPE'):
            key = 'ESC'
        if ((x + len(' '.join((key, label)))) >= self.get_size()[0]):
            x = 0
            y += 1
            if (y > max_y):
                break
        self.legend_win.addstr(y, x, key.upper(), curses.A_REVERSE)
        x += len(key)
        self.legend_win.addstr(y, x, (' ' + label))
        x += (len(label) + 2)
    self.legend_win.refresh()
