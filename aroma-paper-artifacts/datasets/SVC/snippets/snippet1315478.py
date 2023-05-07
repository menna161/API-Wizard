from __future__ import division, absolute_import, print_function
import os
from distutils.msvc9compiler import MSVCCompiler as _MSVCCompiler
from .system_info import platform_bits


def manifest_setup_ldargs(self, output_filename, build_temp, ld_args):
    ld_args.append('/MANIFEST')
    _MSVCCompiler.manifest_setup_ldargs(self, output_filename, build_temp, ld_args)
