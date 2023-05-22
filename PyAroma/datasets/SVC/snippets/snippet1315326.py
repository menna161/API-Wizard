from __future__ import division, absolute_import, print_function
import platform
from distutils.unixccompiler import UnixCCompiler
from numpy.distutils.exec_command import find_executable
from numpy.distutils.ccompiler import simple_version_match
from numpy.distutils.msvc9compiler import MSVCCompiler


def initialize(self, plat_name=None):
    MSVCCompiler.initialize(self, plat_name)
    self.cc = self.find_exe('icl.exe')
    self.lib = self.find_exe('xilib')
    self.linker = self.find_exe('xilink')
    self.compile_options = ['/nologo', '/O3', '/MD', '/W3', '/Qstd=c99']
    self.compile_options_debug = ['/nologo', '/Od', '/MDd', '/W3', '/Qstd=c99', '/Z7', '/D_DEBUG']
