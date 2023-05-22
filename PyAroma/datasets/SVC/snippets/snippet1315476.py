from __future__ import division, absolute_import, print_function
import os
from distutils.msvc9compiler import MSVCCompiler as _MSVCCompiler
from .system_info import platform_bits


def __init__(self, verbose=0, dry_run=0, force=0):
    _MSVCCompiler.__init__(self, verbose, dry_run, force)
