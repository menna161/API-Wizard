from __future__ import division, absolute_import, print_function
import os
import sys
import subprocess
import re
import numpy.distutils.ccompiler
import distutils.cygwinccompiler
from distutils.version import StrictVersion
from numpy.distutils.ccompiler import gen_preprocess_options, gen_lib_options
from distutils.unixccompiler import UnixCCompiler
from distutils.msvccompiler import get_build_version as get_build_msvc_version
from distutils.errors import DistutilsExecError, CompileError, UnknownFileError
from numpy.distutils.misc_util import msvc_runtime_library, msvc_runtime_version, msvc_runtime_major, get_build_architecture
from . import log
from numpy.distutils import log
from numpy.distutils import lib2def
import msvcrt


def build_msvcr_library(debug=False):
    if (os.name != 'nt'):
        return False
    msvcr_ver = msvc_runtime_major()
    if (msvcr_ver is None):
        log.debug('Skip building import library: Runtime is not compiled with MSVC')
        return False
    if (msvcr_ver < 80):
        log.debug('Skip building msvcr library: custom functionality not present')
        return False
    msvcr_name = msvc_runtime_library()
    if debug:
        msvcr_name += 'd'
    out_name = ('lib%s.a' % msvcr_name)
    out_file = os.path.join(sys.prefix, 'libs', out_name)
    if os.path.isfile(out_file):
        log.debug(('Skip building msvcr library: "%s" exists' % (out_file,)))
        return True
    msvcr_dll_name = (msvcr_name + '.dll')
    dll_file = find_dll(msvcr_dll_name)
    if (not dll_file):
        log.warn(('Cannot build msvcr library: "%s" not found' % msvcr_dll_name))
        return False
    def_name = ('lib%s.def' % msvcr_name)
    def_file = os.path.join(sys.prefix, 'libs', def_name)
    log.info(('Building msvcr library: "%s" (from %s)' % (out_file, dll_file)))
    generate_def(dll_file, def_file)
    cmd = ['dlltool', '-d', def_file, '-l', out_file]
    retcode = subprocess.call(cmd)
    os.remove(def_file)
    return (not retcode)
