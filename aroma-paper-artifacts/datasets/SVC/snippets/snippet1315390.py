from __future__ import division, absolute_import, print_function
import os
import re
import sys
import copy
import glob
import atexit
import tempfile
import subprocess
import shutil
import multiprocessing
import distutils
from distutils.errors import DistutilsError
from numpy.distutils.compat import get_exception
from numpy.compat import basestring
from numpy.compat import npy_load_module
from threading import local as tlocal
from numpy.distutils.core import get_distribution
import numpy
from numpy.distutils.npy_pkg_config import read_config
from numpy.distutils.npy_pkg_config import parse_flags
import warnings
from numpy.distutils.system_info import system_info
from distutils.dir_util import mkpath
from distutils.msvccompiler import get_build_architecture
from dummy_threading import local as tlocal
from numpy.distutils.core import get_distribution
from numpy.distutils.core import Extension
from pprint import pformat
from .system_info import get_info, dict_append
import distutils.core
import numpy
import builtins
import __builtin__ as builtins
import curses
from numpy.distutils.core import Extension
from distutils.errors import DistutilsInternalError


def msvc_runtime_library():
    'Return name of MSVC runtime library if Python was built with MSVC >= 7'
    ver = msvc_runtime_major()
    if ver:
        if (ver < 140):
            return ('msvcr%i' % ver)
        else:
            return ('vcruntime%i' % ver)
    else:
        return None
