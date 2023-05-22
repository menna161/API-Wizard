import os
import importlib.util
import sys
from glob import glob
from distutils.core import Command
from distutils.errors import *
from distutils.util import convert_path, Mixin2to3
from distutils import log
from distutils.util import byte_compile


def get_source_files(self):
    return [module[(- 1)] for module in self.find_all_modules()]
