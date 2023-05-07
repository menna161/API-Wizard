import os
import subprocess
import sys
import re
from distutils.errors import DistutilsExecError, DistutilsPlatformError, CompileError, LibError, LinkError
from distutils.ccompiler import CCompiler, gen_preprocess_options, gen_lib_options
from distutils import log
from distutils.util import get_platform
import winreg


def runtime_library_dir_option(self, dir):
    raise DistutilsPlatformError("don't know how to set runtime library search path for MSVC++")
