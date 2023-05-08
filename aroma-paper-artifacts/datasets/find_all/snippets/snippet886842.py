import os
import re
import sys
import curses
import logging
from . import helpers
from .line import Line
from .cursor import Cursor
from .themes import scope_to_pair
import suplemon.linelight
import importlib
import pygments.lexers
from .lexer import Lexer


def __init__(self, app, window):
    '\n        Handle Viewer initialization\n\n        :param App app: The main App class of Suplemon\n        :param Window window: The ui window to use for the viewer\n        '
    self.app = app
    self.window = window
    self.logger = logging.getLogger(__name__)
    self.config = {}
    self.data = ''
    self.lines = [Line()]
    self.file_extension = ''
    self.extension_map = {'scss': 'css', 'less': 'css', 'tmtheme': 'xml', 'ts': 'js'}
    self.show_line_ends = True
    self.cursor_style = curses.A_UNDERLINE
    self.y_scroll = 0
    self.x_scroll = 0
    self.cursors = [Cursor()]
    self.buffer = []
    self.last_find = ''
    self.operations = {'arrow_right': self.arrow_right, 'arrow_left': self.arrow_left, 'arrow_up': self.arrow_up, 'arrow_down': self.arrow_down, 'jump_left': self.jump_left, 'jump_right': self.jump_right, 'jump_up': self.jump_up, 'jump_down': self.jump_down, 'page_up': self.page_up, 'page_down': self.page_down, 'home': self.home, 'end': self.end, 'find': self.find_query, 'find_next': self.find_next, 'find_all': self.find_all}
    self.pygments_syntax = None
    self.lexer = None
