import re
from re import escape
from os.path import commonprefix
from itertools import groupby
from operator import itemgetter


def regex_opt_inner(strings, open_paren):
    'Return a regex that matches any string in the sorted list of strings.'
    close_paren = ((open_paren and ')') or '')
    if (not strings):
        return ''
    first = strings[0]
    if (len(strings) == 1):
        return ((open_paren + escape(first)) + close_paren)
    if (not first):
        return (((open_paren + regex_opt_inner(strings[1:], '(?:')) + '?') + close_paren)
    if (len(first) == 1):
        oneletter = []
        rest = []
        for s in strings:
            if (len(s) == 1):
                oneletter.append(s)
            else:
                rest.append(s)
        if (len(oneletter) > 1):
            if rest:
                return ((((open_paren + regex_opt_inner(rest, '')) + '|') + make_charset(oneletter)) + close_paren)
            return ((open_paren + make_charset(oneletter)) + close_paren)
    prefix = commonprefix(strings)
    if prefix:
        plen = len(prefix)
        return (((open_paren + escape(prefix)) + regex_opt_inner([s[plen:] for s in strings], '(?:')) + close_paren)
    strings_rev = [s[::(- 1)] for s in strings]
    suffix = commonprefix(strings_rev)
    if suffix:
        slen = len(suffix)
        return (((open_paren + regex_opt_inner(sorted((s[:(- slen)] for s in strings)), '(?:')) + escape(suffix[::(- 1)])) + close_paren)
    return ((open_paren + '|'.join((regex_opt_inner(list(group[1]), '') for group in groupby(strings, (lambda s: (s[0] == first[0])))))) + close_paren)
