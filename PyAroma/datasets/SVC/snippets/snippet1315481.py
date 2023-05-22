from __future__ import division, absolute_import, print_function
import os
from distutils.msvccompiler import MSVCCompiler as _MSVCCompiler
from .system_info import platform_bits


def initialize(self):
    environ_lib = os.getenv('lib', '')
    environ_include = os.getenv('include', '')
    _MSVCCompiler.initialize(self)
    os.environ['lib'] = _merge(environ_lib, os.environ['lib'])
    os.environ['include'] = _merge(environ_include, os.environ['include'])
    if (platform_bits == 32):
        self.compile_options += ['/arch:SSE2']
        self.compile_options_debug += ['/arch:SSE2']
