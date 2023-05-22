import os, re
import fnmatch
import functools
from distutils.util import convert_path
from distutils.errors import DistutilsTemplateError, DistutilsInternalError
from distutils import log
from distutils.debug import DEBUG


def findall(dir=os.curdir):
    "\n    Find all files under 'dir' and return the list of full filenames.\n    Unless dir is '.', return full filenames with dir prepended.\n    "
    files = _find_all_simple(dir)
    if (dir == os.curdir):
        make_rel = functools.partial(os.path.relpath, start=dir)
        files = map(make_rel, files)
    return list(files)
