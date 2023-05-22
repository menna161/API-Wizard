import os
import functools
import distutils.core
import distutils.filelist
from distutils.util import convert_path
from fnmatch import fnmatchcase
from setuptools.extern.six.moves import filter, map
import setuptools.version
from setuptools.extension import Extension
from setuptools.dist import Distribution, Feature
from setuptools.depends import Require
from . import monkey


def findall(dir=os.curdir):
    "\n    Find all files under 'dir' and return the list of full filenames.\n    Unless dir is '.', return full filenames with dir prepended.\n    "
    files = _find_all_simple(dir)
    if (dir == os.curdir):
        make_rel = functools.partial(os.path.relpath, start=dir)
        files = map(make_rel, files)
    return list(files)
