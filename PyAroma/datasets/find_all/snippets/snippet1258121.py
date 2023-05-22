import os
import importlib.util
import sys
from glob import glob
from distutils.core import Command
from distutils.errors import *
from distutils.util import convert_path, Mixin2to3
from distutils import log
from distutils.util import byte_compile


def get_outputs(self, include_bytecode=1):
    modules = self.find_all_modules()
    outputs = []
    for (package, module, module_file) in modules:
        package = package.split('.')
        filename = self.get_module_outfile(self.build_lib, package, module)
        outputs.append(filename)
        if include_bytecode:
            if self.compile:
                outputs.append(importlib.util.cache_from_source(filename, optimization=''))
            if (self.optimize > 0):
                outputs.append(importlib.util.cache_from_source(filename, optimization=self.optimize))
    outputs += [os.path.join(build_dir, filename) for (package, src_dir, build_dir, filenames) in self.data_files for filename in filenames]
    return outputs
