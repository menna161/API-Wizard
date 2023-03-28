from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import re
import sys
from xml.etree import ElementTree
from collections import Counter, OrderedDict


def format_value(value, datatype):
    "\n    Format a value for a CSV file, escaping double quotes and backslashes.\n\n    None maps to empty.\n\n    datatype should be\n        's' for string (escaped)\n        'n' for number\n        'd' for datetime\n    "
    if (value is None):
        return ''
    elif (datatype == 's'):
        return ('"%s"' % value.replace('\\', '\\\\').replace('"', '\\"'))
    elif (datatype in ('n', 'd')):
        return value
    else:
        raise KeyError(('Unexpected format value: %s' % datatype))
