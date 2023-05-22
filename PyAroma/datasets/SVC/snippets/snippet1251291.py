import os
import shutil
import stat
import subprocess
import winreg
from distutils.errors import DistutilsExecError, DistutilsPlatformError, CompileError, LibError, LinkError
from distutils.ccompiler import CCompiler, gen_lib_options
from distutils import log
from distutils.util import get_platform
from itertools import count
import _distutils_findvs
import threading
import glob


def _find_vcvarsall(plat_spec):
    (best_version, best_dir) = _find_vc2017()
    vcruntime = None
    vcruntime_plat = ('x64' if ('amd64' in plat_spec) else 'x86')
    if best_version:
        vcredist = os.path.join(best_dir, '..', '..', 'redist', 'MSVC', '**', 'Microsoft.VC141.CRT', 'vcruntime140.dll')
        try:
            import glob
            vcruntime = glob.glob(vcredist, recursive=True)[(- 1)]
        except (ImportError, OSError, LookupError):
            vcruntime = None
    if (not best_version):
        (best_version, best_dir) = _find_vc2015()
        if best_version:
            vcruntime = os.path.join(best_dir, 'redist', vcruntime_plat, 'Microsoft.VC140.CRT', 'vcruntime140.dll')
    if (not best_version):
        log.debug('No suitable Visual C++ version found')
        return (None, None)
    vcvarsall = os.path.join(best_dir, 'vcvarsall.bat')
    if (not os.path.isfile(vcvarsall)):
        log.debug('%s cannot be found', vcvarsall)
        return (None, None)
    if ((not vcruntime) or (not os.path.isfile(vcruntime))):
        log.debug('%s cannot be found', vcruntime)
        vcruntime = None
    return (vcvarsall, vcruntime)
