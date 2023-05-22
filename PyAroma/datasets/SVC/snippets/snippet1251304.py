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


def runtime_library_dir_option(self, dir):
    raise DistutilsPlatformError("don't know how to set runtime library search path for MSVC")
