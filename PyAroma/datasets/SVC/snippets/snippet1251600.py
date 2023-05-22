import sys, os
from distutils.errors import DistutilsExecError, DistutilsPlatformError, CompileError, LibError, LinkError
from distutils.ccompiler import CCompiler, gen_preprocess_options, gen_lib_options
from distutils import log
import winreg
from distutils.msvc9compiler import MSVCCompiler
from distutils.msvc9compiler import MacroExpander
import win32api
import win32con


def set_path_env_var(self, name):
    "Set environment variable 'name' to an MSVC path type value.\n\n        This is equivalent to a SET command prior to execution of spawned\n        commands.\n        "
    if (name == 'lib'):
        p = self.get_msvc_paths('library')
    else:
        p = self.get_msvc_paths(name)
    if p:
        os.environ[name] = ';'.join(p)
