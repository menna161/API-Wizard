import os, re
import fnmatch
import functools
from distutils.util import convert_path
from distutils.errors import DistutilsTemplateError, DistutilsInternalError
from distutils import log
from distutils.debug import DEBUG


def _find_all_simple(path):
    "\n    Find all files under 'path'\n    "
    results = (os.path.join(base, file) for (base, dirs, files) in os.walk(path, followlinks=True) for file in files)
    return filter(os.path.isfile, results)
