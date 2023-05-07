from ctypes import *
from ctypes.util import find_library
from functools import wraps
import sys
import os
import threading
import string


def nvmlDeviceGetDriverModel(handle):
    c_currModel = _nvmlDriverModel_t()
    c_pendingModel = _nvmlDriverModel_t()
    fn = _nvmlGetFunctionPointer('nvmlDeviceGetDriverModel')
    ret = fn(handle, byref(c_currModel), byref(c_pendingModel))
    _nvmlCheckReturn(ret)
    return [c_currModel.value, c_pendingModel.value]
