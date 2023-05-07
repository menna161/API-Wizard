import sys, os, re
from distutils.errors import *
from distutils.spawn import spawn
from distutils.file_util import move_file
from distutils.dir_util import mkpath
from distutils.dep_util import newer_pairwise, newer_group
from distutils.util import split_quoted, execute
from distutils import log
from distutils.fancy_getopt import FancyGetopt
import tempfile
from distutils.debug import DEBUG


def new_compiler(plat=None, compiler=None, verbose=0, dry_run=0, force=0):
    'Generate an instance of some CCompiler subclass for the supplied\n    platform/compiler combination.  \'plat\' defaults to \'os.name\'\n    (eg. \'posix\', \'nt\'), and \'compiler\' defaults to the default compiler\n    for that platform.  Currently only \'posix\' and \'nt\' are supported, and\n    the default compilers are "traditional Unix interface" (UnixCCompiler\n    class) and Visual C++ (MSVCCompiler class).  Note that it\'s perfectly\n    possible to ask for a Unix compiler object under Windows, and a\n    Microsoft compiler object under Unix -- if you supply a value for\n    \'compiler\', \'plat\' is ignored.\n    '
    if (plat is None):
        plat = os.name
    try:
        if (compiler is None):
            compiler = get_default_compiler(plat)
        (module_name, class_name, long_description) = compiler_class[compiler]
    except KeyError:
        msg = ("don't know how to compile C/C++ code on platform '%s'" % plat)
        if (compiler is not None):
            msg = (msg + (" with '%s' compiler" % compiler))
        raise DistutilsPlatformError(msg)
    try:
        module_name = ('distutils.' + module_name)
        __import__(module_name)
        module = sys.modules[module_name]
        klass = vars(module)[class_name]
    except ImportError:
        raise DistutilsModuleError(("can't compile C/C++ code: unable to load module '%s'" % module_name))
    except KeyError:
        raise DistutilsModuleError(("can't compile C/C++ code: unable to find class '%s' in module '%s'" % (class_name, module_name)))
    return klass(None, dry_run, force)
