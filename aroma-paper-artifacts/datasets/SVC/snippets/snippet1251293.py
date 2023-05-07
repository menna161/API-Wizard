import os
import shutil
import stat
import subprocess
import winreg
from distutils.errors import DistutilsExecError, DistutilsPlatformError, CompileError, LibError, LinkError
from distutils.ccompiler import CCompiler, gen_lib_options
from distutils import log
from distutils.util import get_platform
from itertools import count
import _distutils_findvs
import threading
import glob


def _find_exe(exe, paths=None):
    "Return path to an MSVC executable program.\n\n    Tries to find the program in several places: first, one of the\n    MSVC program search paths from the registry; next, the directories\n    in the PATH environment variable.  If any of those work, return an\n    absolute path that is known to exist.  If none of them work, just\n    return the original program name, 'exe'.\n    "
    if (not paths):
        paths = os.getenv('path').split(os.pathsep)
    for p in paths:
        fn = os.path.join(os.path.abspath(p), exe)
        if os.path.isfile(fn):
            return fn
    return exe
