import os, shutil, traceback
from multiprocessing import Pool
from datetime import datetime
from .cprint import cprint
from .utils import copytree2, AppDataUtil, Cache


def set_static_file_created(self, trimed_path, fullpath):
    ' Set static file is modified in Cache\n\t\t'
    self.sf_mtimes[trimed_path] = datetime.now().timestamp()
    self.generation_result[(- 1)][0].append(('/' + trimed_path))
    cprint.line(('/%s [Asset]' % trimed_path))
