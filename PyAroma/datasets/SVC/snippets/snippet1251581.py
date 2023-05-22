import sys, os
from distutils.errors import DistutilsExecError, DistutilsPlatformError, CompileError, LibError, LinkError
from distutils.ccompiler import CCompiler, gen_preprocess_options, gen_lib_options
from distutils import log
import winreg
from distutils.msvc9compiler import MSVCCompiler
from distutils.msvc9compiler import MacroExpander
import win32api
import win32con


def get_build_version():
    'Return the version of MSVC that was used to build Python.\n\n    For Python 2.3 and up, the version number is included in\n    sys.version.  For earlier versions, assume the compiler is MSVC 6.\n    '
    prefix = 'MSC v.'
    i = sys.version.find(prefix)
    if (i == (- 1)):
        return 6
    i = (i + len(prefix))
    (s, rest) = sys.version[i:].split(' ', 1)
    majorVersion = (int(s[:(- 2)]) - 6)
    if (majorVersion >= 13):
        majorVersion += 1
    minorVersion = (int(s[2:3]) / 10.0)
    if (majorVersion == 6):
        minorVersion = 0
    if (majorVersion >= 6):
        return (majorVersion + minorVersion)
    return None
