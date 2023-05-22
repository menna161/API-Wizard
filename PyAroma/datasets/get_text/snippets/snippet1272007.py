import os
import re
import sys
import textwrap
from string import Formatter
from pathlib import Path
from IPython.utils import py3compat


def get_text_list(list_, last_sep=' and ', sep=', ', wrap_item_with=''):
    '\n    Return a string with a natural enumeration of items\n\n    >>> get_text_list([\'a\', \'b\', \'c\', \'d\'])\n    \'a, b, c and d\'\n    >>> get_text_list([\'a\', \'b\', \'c\'], \' or \')\n    \'a, b or c\'\n    >>> get_text_list([\'a\', \'b\', \'c\'], \', \')\n    \'a, b, c\'\n    >>> get_text_list([\'a\', \'b\'], \' or \')\n    \'a or b\'\n    >>> get_text_list([\'a\'])\n    \'a\'\n    >>> get_text_list([])\n    \'\'\n    >>> get_text_list([\'a\', \'b\'], wrap_item_with="`")\n    \'`a` and `b`\'\n    >>> get_text_list([\'a\', \'b\', \'c\', \'d\'], " = ", sep=" + ")\n    \'a + b + c = d\'\n    '
    if (len(list_) == 0):
        return ''
    if wrap_item_with:
        list_ = [('%s%s%s' % (wrap_item_with, item, wrap_item_with)) for item in list_]
    if (len(list_) == 1):
        return list_[0]
    return ('%s%s%s' % (sep.join((i for i in list_[:(- 1)])), last_sep, list_[(- 1)]))
