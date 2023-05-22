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


def find_all(self):
    'Find all occurances.'
    self.find(self.last_find, True)
