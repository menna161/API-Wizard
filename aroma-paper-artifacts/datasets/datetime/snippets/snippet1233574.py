import re
from hacking import core
import pycodestyle


@core.flake8ext
def use_timeutils_utcnow(logical_line, filename):
    if ('/tools/' in filename):
        return
    msg = 'D705: timeutils.utcnow() must be used instead of datetime.%s()'
    datetime_funcs = ['now', 'utcnow']
    for f in datetime_funcs:
        pos = logical_line.find(('datetime.%s' % f))
        if (pos != (- 1)):
            (yield (pos, (msg % f)))
