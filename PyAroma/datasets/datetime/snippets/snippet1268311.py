from __future__ import unicode_literals
import errno
import sys
import os
import os.path as op
from datetime import datetime
import stat
from .compat import text_type, environb
from .exceptions import TrashPermissionError
from urllib.parse import quote
from urllib import quote


def info_for(src, topdir):
    if ((topdir is None) or (not is_parent(topdir, src))):
        src = op.abspath(src)
    else:
        src = op.relpath(src, topdir)
    info = '[Trash Info]\n'
    info += (('Path=' + quote(src)) + '\n')
    info += (('DeletionDate=' + format_date(datetime.now())) + '\n')
    return info
