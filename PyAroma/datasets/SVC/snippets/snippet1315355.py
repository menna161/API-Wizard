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


def msvc_manifest_xml(maj, min):
    'Given a major and minor version of the MSVCR, returns the\n    corresponding XML file.'
    try:
        fullver = _MSVCRVER_TO_FULLVER[str(((maj * 10) + min))]
    except KeyError:
        raise ValueError(('Version %d,%d of MSVCRT not supported yet' % (maj, min)))
    template = '<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">\n  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">\n    <security>\n      <requestedPrivileges>\n        <requestedExecutionLevel level="asInvoker" uiAccess="false"></requestedExecutionLevel>\n      </requestedPrivileges>\n    </security>\n  </trustInfo>\n  <dependency>\n    <dependentAssembly>\n      <assemblyIdentity type="win32" name="Microsoft.VC%(maj)d%(min)d.CRT" version="%(fullver)s" processorArchitecture="*" publicKeyToken="1fc8b3b9a1e18e3b"></assemblyIdentity>\n    </dependentAssembly>\n  </dependency>\n</assembly>'
    return (template % {'fullver': fullver, 'maj': maj, 'min': min})
