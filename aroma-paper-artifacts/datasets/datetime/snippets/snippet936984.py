import gc
import datetime
import pynvml
import torch
import numpy as np


def __init__(self, frame, detail=True, path='', verbose=False, device=0):
    self.frame = frame
    self.print_detail = detail
    self.last_tensor_sizes = set()
    self.gpu_profile_fn = (path + f'{datetime.datetime.now():%d-%b-%y-%H:%M:%S}-gpu_mem_track.txt')
    self.verbose = verbose
    self.begin = True
    self.device = device
    self.func_name = frame.f_code.co_name
    self.filename = frame.f_globals['__file__']
    if (self.filename.endswith('.pyc') or self.filename.endswith('.pyo')):
        self.filename = self.filename[:(- 1)]
    self.module_name = self.frame.f_globals['__name__']
    self.curr_line = self.frame.f_lineno
