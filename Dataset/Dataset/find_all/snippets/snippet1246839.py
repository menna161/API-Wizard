import dis
import importlib._bootstrap_external
import importlib.machinery
import marshal
import os
import sys
import types
import warnings
import imp
import getopt


def ensure_fromlist(self, m, fromlist, recursive=0):
    self.msg(4, 'ensure_fromlist', m, fromlist, recursive)
    for sub in fromlist:
        if (sub == '*'):
            if (not recursive):
                all = self.find_all_submodules(m)
                if all:
                    self.ensure_fromlist(m, all, 1)
        elif (not hasattr(m, sub)):
            subname = ('%s.%s' % (m.__name__, sub))
            submod = self.import_module(sub, subname, m)
            if (not submod):
                raise ImportError(('No module named ' + subname))
