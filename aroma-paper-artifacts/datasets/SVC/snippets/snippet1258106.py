import contextlib
import os
import re
import sys
from distutils.core import Command
from distutils.errors import *
from distutils.sysconfig import customize_compiler, get_python_version
from distutils.sysconfig import get_config_h_filename
from distutils.dep_util import newer_group
from distutils.extension import Extension
from distutils.util import get_platform
from distutils import log
from site import USER_BASE
from distutils.ccompiler import show_compilers
from distutils import sysconfig
from distutils.ccompiler import new_compiler
from distutils.sysconfig import get_config_var
from concurrent.futures import ThreadPoolExecutor
from distutils._msvccompiler import MSVCCompiler
from distutils import sysconfig


def get_libraries(self, ext):
    "Return the list of libraries to link against when building a\n        shared extension.  On most platforms, this is just 'ext.libraries';\n        on Windows, we add the Python library (eg. python20.dll).\n        "
    if (sys.platform == 'win32'):
        from distutils._msvccompiler import MSVCCompiler
        if (not isinstance(self.compiler, MSVCCompiler)):
            template = 'python%d%d'
            if self.debug:
                template = (template + '_d')
            pythonlib = (template % ((sys.hexversion >> 24), ((sys.hexversion >> 16) & 255)))
            return (ext.libraries + [pythonlib])
        else:
            return ext.libraries
    elif (sys.platform == 'darwin'):
        return ext.libraries
    elif (sys.platform[:3] == 'aix'):
        return ext.libraries
    else:
        from distutils import sysconfig
        if sysconfig.get_config_var('Py_ENABLE_SHARED'):
            pythonlib = 'python{}.{}{}'.format((sys.hexversion >> 24), ((sys.hexversion >> 16) & 255), sysconfig.get_config_var('ABIFLAGS'))
            return (ext.libraries + [pythonlib])
        else:
            return ext.libraries
