import os
import importlib.util
import sys
from glob import glob
from distutils.core import Command
from distutils.errors import *
from distutils.util import convert_path, Mixin2to3
from distutils import log
from distutils.util import byte_compile


def find_all_modules(self):
    "Compute the list of all modules that will be built, whether\n        they are specified one-module-at-a-time ('self.py_modules') or\n        by whole packages ('self.packages').  Return a list of tuples\n        (package, module, module_file), just like 'find_modules()' and\n        'find_package_modules()' do."
    modules = []
    if self.py_modules:
        modules.extend(self.find_modules())
    if self.packages:
        for package in self.packages:
            package_dir = self.get_package_dir(package)
            m = self.find_package_modules(package, package_dir)
            modules.extend(m)
    return modules
