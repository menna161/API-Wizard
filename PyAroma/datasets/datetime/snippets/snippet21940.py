import datetime
import io
from os import linesep
import re
import sys
from pip._vendor.toml.tz import TomlTz
import pathlib
import os
from os import path as op
from warnings import warn


def load_value(self, v, strictly_valid=True):
    if (not v):
        raise ValueError('Empty value is invalid')
    if (v == 'true'):
        return (True, 'bool')
    elif (v == 'false'):
        return (False, 'bool')
    elif ((v[0] == '"') or (v[0] == "'")):
        quotechar = v[0]
        testv = v[1:].split(quotechar)
        triplequote = False
        triplequotecount = 0
        if ((len(testv) > 1) and (testv[0] == '') and (testv[1] == '')):
            testv = testv[2:]
            triplequote = True
        closed = False
        for tv in testv:
            if (tv == ''):
                if triplequote:
                    triplequotecount += 1
                else:
                    closed = True
            else:
                oddbackslash = False
                try:
                    i = (- 1)
                    j = tv[i]
                    while (j == '\\'):
                        oddbackslash = (not oddbackslash)
                        i -= 1
                        j = tv[i]
                except IndexError:
                    pass
                if (not oddbackslash):
                    if closed:
                        raise ValueError('Stuff after closed string. WTF?')
                    elif ((not triplequote) or (triplequotecount > 1)):
                        closed = True
                    else:
                        triplequotecount = 0
        if (quotechar == '"'):
            escapeseqs = v.split('\\')[1:]
            backslash = False
            for i in escapeseqs:
                if (i == ''):
                    backslash = (not backslash)
                else:
                    if ((i[0] not in _escapes) and ((i[0] != 'u') and (i[0] != 'U') and (not backslash))):
                        raise ValueError('Reserved escape sequence used')
                    if backslash:
                        backslash = False
            for prefix in ['\\u', '\\U']:
                if (prefix in v):
                    hexbytes = v.split(prefix)
                    v = _load_unicode_escapes(hexbytes[0], hexbytes[1:], prefix)
            v = _unescape(v)
        if ((len(v) > 1) and (v[1] == quotechar) and ((len(v) < 3) or (v[1] == v[2]))):
            v = v[2:(- 2)]
        return (v[1:(- 1)], 'str')
    elif (v[0] == '['):
        return (self.load_array(v), 'array')
    elif (v[0] == '{'):
        inline_object = self.get_empty_inline_table()
        self.load_inline_object(v, inline_object)
        return (inline_object, 'inline_object')
    elif TIME_RE.match(v):
        (h, m, s, _, ms) = TIME_RE.match(v).groups()
        time = datetime.time(int(h), int(m), int(s), (int(ms) if ms else 0))
        return (time, 'time')
    else:
        parsed_date = _load_date(v)
        if (parsed_date is not None):
            return (parsed_date, 'date')
        if (not strictly_valid):
            raise ValueError('Weirdness with leading zeroes or underscores in your number.')
        itype = 'int'
        neg = False
        if (v[0] == '-'):
            neg = True
            v = v[1:]
        elif (v[0] == '+'):
            v = v[1:]
        v = v.replace('_', '')
        lowerv = v.lower()
        if (('.' in v) or (('x' not in v) and (('e' in v) or ('E' in v)))):
            if (('.' in v) and (v.split('.', 1)[1] == '')):
                raise ValueError('This float is missing digits after the point')
            if (v[0] not in '0123456789'):
                raise ValueError("This float doesn't have a leading digit")
            v = float(v)
            itype = 'float'
        elif ((len(lowerv) == 3) and ((lowerv == 'inf') or (lowerv == 'nan'))):
            v = float(v)
            itype = 'float'
        if (itype == 'int'):
            v = int(v, 0)
        if neg:
            return ((0 - v), itype)
        return (v, itype)
