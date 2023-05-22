import argparse
import codecs
import datetime
import hashlib
import inspect
import logging
import os
import sys
import time
import traceback
import warnings
import dill
import nbformat as nbf
from jupyter_client.kernelspec import KernelSpecManager
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors.execute import CellExecutionError
from pynb.utils import get_func, fatal, check_isfile
from pynb.version import __version__


def process(self, uid, add_footer=False, no_exec=False, disable_cache=False, ignore_cache=False):
    '\n        Execute notebook\n        :return: self\n        '
    self.exec_begin = time.perf_counter()
    self.exec_begin_dt = datetime.datetime.now()
    ep = CachedExecutePreprocessor(timeout=None, kernel_name='python3')
    ep.disable_cache = disable_cache
    ep.ignore_cache = ignore_cache
    ep.uid = uid
    if (not no_exec):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            ep.preprocess(self.nb, {'metadata': {'path': '.'}})
    self.exec_time = (time.perf_counter() - self.exec_begin)
    if add_footer:
        self.add_cell_footer()
    if (not no_exec):
        logging.info('Execution time: {0:.2f}s'.format(self.exec_time))
    return self
