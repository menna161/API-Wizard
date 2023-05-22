import os
import sys
import platform
import itertools
import distutils.errors
from setuptools.extern.packaging.version import LegacyVersion
from setuptools.extern.six.moves import filterfalse
from .monkey import get_unpatched
from setuptools.extern.six.moves import winreg
from distutils.msvc9compiler import Reg
import numpy as np


def _guess_vc(self):
    '\n        Locate Visual C for 2017\n        '
    if (self.vc_ver <= 14.0):
        return
    default = 'VC\\Tools\\MSVC'
    guess_vc = os.path.join(self.VSInstallDir, default)
    try:
        vc_exact_ver = os.listdir(guess_vc)[(- 1)]
        return os.path.join(guess_vc, vc_exact_ver)
    except (OSError, IOError, IndexError):
        pass
