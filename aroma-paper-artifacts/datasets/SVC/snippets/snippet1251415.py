import os
import sys
import copy
from subprocess import Popen, PIPE, check_output
import re
from distutils.ccompiler import gen_preprocess_options, gen_lib_options
from distutils.unixccompiler import UnixCCompiler
from distutils.file_util import write_file
from distutils.errors import DistutilsExecError, CCompilerError, CompileError, UnknownFileError
from distutils import log
from distutils.version import LooseVersion
from distutils.spawn import find_executable
from distutils import sysconfig


def get_msvcr():
    'Include the appropriate MSVC runtime library if Python was built\n    with MSVC 7.0 or later.\n    '
    msc_pos = sys.version.find('MSC v.')
    if (msc_pos != (- 1)):
        msc_ver = sys.version[(msc_pos + 6):(msc_pos + 10)]
        if (msc_ver == '1300'):
            return ['msvcr70']
        elif (msc_ver == '1310'):
            return ['msvcr71']
        elif (msc_ver == '1400'):
            return ['msvcr80']
        elif (msc_ver == '1500'):
            return ['msvcr90']
        elif (msc_ver == '1600'):
            return ['msvcr100']
        else:
            raise ValueError(('Unknown MS Compiler version %s ' % msc_ver))
