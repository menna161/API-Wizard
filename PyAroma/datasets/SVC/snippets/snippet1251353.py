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


def compile(self, sources, output_dir=None, macros=None, include_dirs=None, debug=0, extra_preargs=None, extra_postargs=None, depends=None):
    'Compile one or more source files.\n\n        \'sources\' must be a list of filenames, most likely C/C++\n        files, but in reality anything that can be handled by a\n        particular compiler and compiler class (eg. MSVCCompiler can\n        handle resource files in \'sources\').  Return a list of object\n        filenames, one per source filename in \'sources\'.  Depending on\n        the implementation, not all source files will necessarily be\n        compiled, but all corresponding object filenames will be\n        returned.\n\n        If \'output_dir\' is given, object files will be put under it, while\n        retaining their original path component.  That is, "foo/bar.c"\n        normally compiles to "foo/bar.o" (for a Unix implementation); if\n        \'output_dir\' is "build", then it would compile to\n        "build/foo/bar.o".\n\n        \'macros\', if given, must be a list of macro definitions.  A macro\n        definition is either a (name, value) 2-tuple or a (name,) 1-tuple.\n        The former defines a macro; if the value is None, the macro is\n        defined without an explicit value.  The 1-tuple case undefines a\n        macro.  Later definitions/redefinitions/ undefinitions take\n        precedence.\n\n        \'include_dirs\', if given, must be a list of strings, the\n        directories to add to the default include file search path for this\n        compilation only.\n\n        \'debug\' is a boolean; if true, the compiler will be instructed to\n        output debug symbols in (or alongside) the object file(s).\n\n        \'extra_preargs\' and \'extra_postargs\' are implementation- dependent.\n        On platforms that have the notion of a command-line (e.g. Unix,\n        DOS/Windows), they are most likely lists of strings: extra\n        command-line arguments to prepand/append to the compiler command\n        line.  On other platforms, consult the implementation class\n        documentation.  In any event, they are intended as an escape hatch\n        for those occasions when the abstract compiler framework doesn\'t\n        cut the mustard.\n\n        \'depends\', if given, is a list of filenames that all targets\n        depend on.  If a source file is older than any file in\n        depends, then the source file will be recompiled.  This\n        supports dependency tracking, but only at a coarse\n        granularity.\n\n        Raises CompileError on failure.\n        '
    (macros, objects, extra_postargs, pp_opts, build) = self._setup_compile(output_dir, macros, include_dirs, sources, depends, extra_postargs)
    cc_args = self._get_cc_args(pp_opts, debug, extra_preargs)
    for obj in objects:
        try:
            (src, ext) = build[obj]
        except KeyError:
            continue
        self._compile(obj, src, ext, cc_args, extra_postargs, pp_opts)
    return objects
