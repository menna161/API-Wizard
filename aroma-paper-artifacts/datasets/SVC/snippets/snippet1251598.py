import sys, os
from distutils.errors import DistutilsExecError, DistutilsPlatformError, CompileError, LibError, LinkError
from distutils.ccompiler import CCompiler, gen_preprocess_options, gen_lib_options
from distutils import log
import winreg
from distutils.msvc9compiler import MSVCCompiler
from distutils.msvc9compiler import MacroExpander
import win32api
import win32con


def find_exe(self, exe):
    "Return path to an MSVC executable program.\n\n        Tries to find the program in several places: first, one of the\n        MSVC program search paths from the registry; next, the directories\n        in the PATH environment variable.  If any of those work, return an\n        absolute path that is known to exist.  If none of them work, just\n        return the original program name, 'exe'.\n        "
    for p in self.__paths:
        fn = os.path.join(os.path.abspath(p), exe)
        if os.path.isfile(fn):
            return fn
    for p in os.environ['Path'].split(';'):
        fn = os.path.join(os.path.abspath(p), exe)
        if os.path.isfile(fn):
            return fn
    return exe
