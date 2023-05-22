import datetime
import numbers
import re
import sys
import os
import textwrap
from tornado.escape import _unicode, native_str
from tornado.log import define_logging_options
from tornado.util import basestring_type, exec_in
import typing
from typing import Any, Iterator, Iterable, Tuple, Set, Dict, Callable, List, TextIO
from typing import Optional


def define(self, name: str, default: Any=None, type: type=None, help: str=None, metavar: str=None, multiple: bool=False, group: str=None, callback: Callable[([Any], None)]=None) -> None:
    'Defines a new command line option.\n\n        ``type`` can be any of `str`, `int`, `float`, `bool`,\n        `~datetime.datetime`, or `~datetime.timedelta`. If no ``type``\n        is given but a ``default`` is, ``type`` is the type of\n        ``default``. Otherwise, ``type`` defaults to `str`.\n\n        If ``multiple`` is True, the option value is a list of ``type``\n        instead of an instance of ``type``.\n\n        ``help`` and ``metavar`` are used to construct the\n        automatically generated command line help string. The help\n        message is formatted like::\n\n           --name=METAVAR      help string\n\n        ``group`` is used to group the defined options in logical\n        groups. By default, command line options are grouped by the\n        file in which they are defined.\n\n        Command line option names must be unique globally.\n\n        If a ``callback`` is given, it will be run with the new value whenever\n        the option is changed.  This can be used to combine command-line\n        and file-based options::\n\n            define("config", type=str, help="path to config file",\n                   callback=lambda path: parse_config_file(path, final=False))\n\n        With this definition, options in the file specified by ``--config`` will\n        override options set earlier on the command line, but can be overridden\n        by later flags.\n\n        '
    normalized = self._normalize_name(name)
    if (normalized in self._options):
        raise Error(('Option %r already defined in %s' % (normalized, self._options[normalized].file_name)))
    frame = sys._getframe(0)
    options_file = frame.f_code.co_filename
    if ((frame.f_back.f_code.co_filename == options_file) and (frame.f_back.f_code.co_name == 'define')):
        frame = frame.f_back
    file_name = frame.f_back.f_code.co_filename
    if (file_name == options_file):
        file_name = ''
    if (type is None):
        if ((not multiple) and (default is not None)):
            type = default.__class__
        else:
            type = str
    if group:
        group_name = group
    else:
        group_name = file_name
    option = _Option(name, file_name=file_name, default=default, type=type, help=help, metavar=metavar, multiple=multiple, group_name=group_name, callback=callback)
    self._options[normalized] = option
