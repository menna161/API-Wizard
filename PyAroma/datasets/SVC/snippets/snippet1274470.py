import os, sys, io
from . import ffiplatform, model
from .error import VerificationError
from .cffi_opcode import *
from distutils.command.build_ext import build_ext
from testing.udir import udir
import imp
from distutils.msvc9compiler import MSVCCompiler
from distutils.ccompiler import CCompiler


def _patch_for_embedding(patchlist):
    if (sys.platform == 'win32'):
        from distutils.msvc9compiler import MSVCCompiler
        _patch_meth(patchlist, MSVCCompiler, '_remove_visual_c_ref', (lambda self, manifest_file: manifest_file))
    if (sys.platform == 'darwin'):
        from distutils.ccompiler import CCompiler

        def my_link_shared_object(self, *args, **kwds):
            if ('-bundle' in self.linker_so):
                self.linker_so = list(self.linker_so)
                i = self.linker_so.index('-bundle')
                self.linker_so[i] = '-dynamiclib'
            return old_link_shared_object(self, *args, **kwds)
        old_link_shared_object = _patch_meth(patchlist, CCompiler, 'link_shared_object', my_link_shared_object)
