import string, re, sys, datetime
from .core import TomlError
from .utils import rfc3339_re, parse_rfc3339_re


def _p_value(s, object_pairs_hook):
    pos = s.pos()
    if s.consume('true'):
        return ('bool', s.last(), True, pos)
    if s.consume('false'):
        return ('bool', s.last(), False, pos)
    if s.consume('"'):
        if s.consume('""'):
            r = _p_basicstr_content(s, _basicstr_ml_re)
            s.expect('"""')
        else:
            r = _p_basicstr_content(s, _basicstr_re)
            s.expect('"')
        return ('str', r, r, pos)
    if s.consume("'"):
        if s.consume("''"):
            r = s.expect_re(_litstr_ml_re).group(0)
            s.expect("'''")
        else:
            r = s.expect_re(_litstr_re).group(0)
            s.expect("'")
        return ('str', r, r, pos)
    if s.consume_re(rfc3339_re):
        m = s.last()
        return ('datetime', m.group(0), parse_rfc3339_re(m), pos)
    if s.consume_re(_float_re):
        m = s.last().group(0)
        r = m.replace('_', '')
        if (('.' in m) or ('e' in m) or ('E' in m)):
            return ('float', m, float(r), pos)
        else:
            return ('int', m, int(r, 10), pos)
    if s.consume('['):
        items = []
        with s:
            while True:
                _p_ews(s)
                items.append(_p_value(s, object_pairs_hook=object_pairs_hook))
                s.commit()
                _p_ews(s)
                s.expect(',')
                s.commit()
        _p_ews(s)
        s.expect(']')
        return ('array', None, items, pos)
    if s.consume('{'):
        _p_ws(s)
        items = object_pairs_hook()
        if (not s.consume('}')):
            k = _p_key(s)
            _p_ws(s)
            s.expect('=')
            _p_ws(s)
            items[k] = _p_value(s, object_pairs_hook=object_pairs_hook)
            _p_ws(s)
            while s.consume(','):
                _p_ws(s)
                k = _p_key(s)
                _p_ws(s)
                s.expect('=')
                _p_ws(s)
                items[k] = _p_value(s, object_pairs_hook=object_pairs_hook)
                _p_ws(s)
            s.expect('}')
        return ('table', None, items, pos)
    s.fail()
