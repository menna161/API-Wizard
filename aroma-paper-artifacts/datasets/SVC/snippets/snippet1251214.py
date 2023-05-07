import os
import shutil
import subprocess
import sys
from ctypes import cdll
import importlib.machinery
from ctypes.macholib.dyld import dyld_find as _dyld_find
from ctypes._aix import find_library
import re, tempfile
from ctypes import CDLL
import struct


def _get_build_version():
    'Return the version of MSVC that was used to build Python.\n\n        For Python 2.3 and up, the version number is included in\n        sys.version.  For earlier versions, assume the compiler is MSVC 6.\n        '
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
