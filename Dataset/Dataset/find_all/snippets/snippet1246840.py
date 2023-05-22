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


def find_all_submodules(self, m):
    if (not m.__path__):
        return
    modules = {}
    suffixes = []
    suffixes += importlib.machinery.EXTENSION_SUFFIXES[:]
    suffixes += importlib.machinery.SOURCE_SUFFIXES[:]
    suffixes += importlib.machinery.BYTECODE_SUFFIXES[:]
    for dir in m.__path__:
        try:
            names = os.listdir(dir)
        except OSError:
            self.msg(2, "can't list directory", dir)
            continue
        for name in names:
            mod = None
            for suff in suffixes:
                n = len(suff)
                if (name[(- n):] == suff):
                    mod = name[:(- n)]
                    break
            if (mod and (mod != '__init__')):
                modules[mod] = mod
    return modules.keys()
