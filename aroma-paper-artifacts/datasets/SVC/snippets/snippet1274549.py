import os, sys, io
from . import ffiplatform, model
from .error import VerificationError
from .cffi_opcode import *
from distutils.command.build_ext import build_ext
from testing.udir import udir
import imp
from distutils.msvc9compiler import MSVCCompiler
from distutils.ccompiler import CCompiler


def _print_string_literal_in_array(self, s):
    prnt = self._prnt
    prnt('// # NB. this is not a string because of a size limit in MSVC')
    for line in s.splitlines(True):
        prnt(('// ' + line).rstrip())
        printed_line = ''
        for c in line:
            if (len(printed_line) >= 76):
                prnt(printed_line)
                printed_line = ''
            printed_line += ('%d,' % (ord(c),))
        prnt(printed_line)
