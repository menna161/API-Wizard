from __future__ import unicode_literals
import io, datetime, math, string, sys
from .utils import format_rfc3339


def _format_value(v):
    if isinstance(v, bool):
        return ('true' if v else 'false')
    if (isinstance(v, int) or isinstance(v, long)):
        return unicode(v)
    if isinstance(v, float):
        if (math.isnan(v) or math.isinf(v)):
            raise ValueError('{0} is not a valid TOML value'.format(v))
        else:
            return repr(v)
    elif (isinstance(v, unicode) or isinstance(v, bytes)):
        return _escape_string(v)
    elif isinstance(v, datetime.datetime):
        return format_rfc3339(v)
    elif isinstance(v, list):
        return '[{0}]'.format(', '.join((_format_value(obj) for obj in v)))
    elif isinstance(v, dict):
        return '{{{0}}}'.format(', '.join(('{} = {}'.format(_escape_id(k), _format_value(obj)) for (k, obj) in v.items())))
    else:
        raise RuntimeError(v)
