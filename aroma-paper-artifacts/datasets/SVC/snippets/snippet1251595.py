import sys, os
from distutils.errors import DistutilsExecError, DistutilsPlatformError, CompileError, LibError, LinkError
from distutils.ccompiler import CCompiler, gen_preprocess_options, gen_lib_options
from distutils import log
import winreg
from distutils.msvc9compiler import MSVCCompiler
from distutils.msvc9compiler import MacroExpander
import win32api
import win32con


def runtime_library_dir_option(self, dir):
    raise DistutilsPlatformError("don't know how to set runtime library search path for MSVC++")
