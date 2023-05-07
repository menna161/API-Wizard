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


def __init__(self, verbose=0, dry_run=0, force=0):
    distutils.cygwinccompiler.CygwinCCompiler.__init__(self, verbose, dry_run, force)
    if (self.gcc_version is None):
        p = subprocess.Popen(['gcc', '-dumpversion'], shell=True, stdout=subprocess.PIPE)
        out_string = p.stdout.read()
        p.stdout.close()
        result = re.search('(\\d+\\.\\d+)', out_string)
        if result:
            self.gcc_version = StrictVersion(result.group(1))
    if (self.gcc_version <= '2.91.57'):
        entry_point = '--entry _DllMain@12'
    else:
        entry_point = ''
    if (self.linker_dll == 'dllwrap'):
        self.linker = 'dllwrap'
    elif (self.linker_dll == 'gcc'):
        self.linker = 'g++'
    build_import_library()
    msvcr_success = build_msvcr_library()
    msvcr_dbg_success = build_msvcr_library(debug=True)
    if (msvcr_success or msvcr_dbg_success):
        self.define_macro('NPY_MINGW_USE_CUSTOM_MSVCR')
    msvcr_version = msvc_runtime_version()
    if msvcr_version:
        self.define_macro('__MSVCRT_VERSION__', ('0x%04i' % msvcr_version))
    if (get_build_architecture() == 'AMD64'):
        if (self.gcc_version < '4.0'):
            self.set_executables(compiler='gcc -g -DDEBUG -DMS_WIN64 -mno-cygwin -O0 -Wall', compiler_so='gcc -g -DDEBUG -DMS_WIN64 -mno-cygwin -O0 -Wall -Wstrict-prototypes', linker_exe='gcc -g -mno-cygwin', linker_so='gcc -g -mno-cygwin -shared')
        else:
            self.set_executables(compiler='gcc -g -DDEBUG -DMS_WIN64 -O0 -Wall', compiler_so='gcc -g -DDEBUG -DMS_WIN64 -O0 -Wall -Wstrict-prototypes', linker_exe='gcc -g', linker_so='gcc -g -shared')
    elif (self.gcc_version <= '3.0.0'):
        self.set_executables(compiler='gcc -mno-cygwin -O2 -w', compiler_so='gcc -mno-cygwin -mdll -O2 -w -Wstrict-prototypes', linker_exe='g++ -mno-cygwin', linker_so=('%s -mno-cygwin -mdll -static %s' % (self.linker, entry_point)))
    elif (self.gcc_version < '4.0'):
        self.set_executables(compiler='gcc -mno-cygwin -O2 -Wall', compiler_so='gcc -mno-cygwin -O2 -Wall -Wstrict-prototypes', linker_exe='g++ -mno-cygwin', linker_so='g++ -mno-cygwin -shared')
    else:
        self.set_executables(compiler='gcc -O2 -Wall', compiler_so='gcc -O2 -Wall -Wstrict-prototypes', linker_exe='g++ ', linker_so='g++ -shared')
    self.compiler_cxx = ['g++']
    return
