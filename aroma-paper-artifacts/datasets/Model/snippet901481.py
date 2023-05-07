from ctypes import *
from ctypes.util import find_library
from functools import wraps
import sys
import os
import threading
import string


def nvmlDeviceSetDriverModel(handle, model):
    fn = _nvmlGetFunctionPointer('nvmlDeviceSetDriverModel')
    ret = fn(handle, _nvmlDriverModel_t(model))
    _nvmlCheckReturn(ret)
    return None
