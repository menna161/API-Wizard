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


def _find_all_simple(path):
    "\n    Find all files under 'path'\n    "
    results = (os.path.join(base, file) for (base, dirs, files) in os.walk(path, followlinks=True) for file in files)
    return filter(os.path.isfile, results)
