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


@property
def WindowsSdkVersion(self):
    '\n        Microsoft Windows SDK versions for specified MSVC++ version.\n        '
    if (self.vc_ver <= 9.0):
        return ('7.0', '6.1', '6.0a')
    elif (self.vc_ver == 10.0):
        return ('7.1', '7.0a')
    elif (self.vc_ver == 11.0):
        return ('8.0', '8.0a')
    elif (self.vc_ver == 12.0):
        return ('8.1', '8.1a')
    elif (self.vc_ver >= 14.0):
        return ('10.0', '8.1')
