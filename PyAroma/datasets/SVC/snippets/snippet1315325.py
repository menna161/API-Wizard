from __future__ import division, absolute_import, print_function
import platform
from distutils.unixccompiler import UnixCCompiler
from numpy.distutils.exec_command import find_executable
from numpy.distutils.ccompiler import simple_version_match
from numpy.distutils.msvc9compiler import MSVCCompiler


def __init__(self, verbose=0, dry_run=0, force=0):
    MSVCCompiler.__init__(self, verbose, dry_run, force)
    version_match = simple_version_match(start='Intel\\(R\\).*?32,')
    self.__version = version_match
