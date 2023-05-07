import re
import io
import datetime
from os import linesep
import sys
from os import path as op
from warnings import warn


def _load_date(val):
    microsecond = 0
    tz = None
    try:
        if (len(val) > 19):
            if (val[19] == '.'):
                if (val[(- 1)].upper() == 'Z'):
                    subsecondval = val[20:(- 1)]
                    tzval = 'Z'
                else:
                    subsecondvalandtz = val[20:]
                    if ('+' in subsecondvalandtz):
                        splitpoint = subsecondvalandtz.index('+')
                        subsecondval = subsecondvalandtz[:splitpoint]
                        tzval = subsecondvalandtz[splitpoint:]
                    elif ('-' in subsecondvalandtz):
                        splitpoint = subsecondvalandtz.index('-')
                        subsecondval = subsecondvalandtz[:splitpoint]
                        tzval = subsecondvalandtz[splitpoint:]
                tz = TomlTz(tzval)
                microsecond = int((int(subsecondval) * (10 ** (6 - len(subsecondval)))))
            else:
                tz = TomlTz(val[19:])
    except ValueError:
        tz = None
    if ('-' not in val[1:]):
        return None
    try:
        d = datetime.datetime(int(val[:4]), int(val[5:7]), int(val[8:10]), int(val[11:13]), int(val[14:16]), int(val[17:19]), microsecond, tz)
    except ValueError:
        return None
    return d
