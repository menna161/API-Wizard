import os
import numpy as np
import ctypes
import subprocess
from .pre_process import para_preprocess


def __init__(self, system_type='Windows', seed=0):
    '\n        The basic class for sampling distribution on cpu\n        '
    super(model_sampler_gpu, self).__init__()
    self.system_type = system_type
    self.seed = seed
    if (system_type == 'Windows'):
        '\n            To compile CUDA C/C++ under Windows system, Visual Studio and CUDA should have been installed.\n            This module has been tested under Visual Studio 2019(with MSVC v142 - VS 2019 C++ x64/x86 tools) and CUDA Toolkit 11.5.\n            '
        compact_path = (os.path.dirname(__file__) + '\\_compact\\model_sampler.dll')
        if (not os.path.exists(compact_path)):
            install_flag = subprocess.call((((((((('nvcc -o ' + '"') + compact_path) + '"') + ' --shared ') + '"') + compact_path[:(- 4)]) + '_win.cu') + '"'), shell=True)
            if (install_flag != 0):
                search_flag = os.system('where nvcc')
                if (search_flag != 0):
                    Warning('Could not locate the path of nvcc, please make sure nvcc can be located by the system command "where nvcc"')
                else:
                    path_results = subprocess.check_output('where nvcc', shell=True)
                    path_results = str(path_results, encoding='utf-8')
                    nvcc_path = path_results.split('\n')[0]
                    nvcc_path = (nvcc_path[:nvcc_path.find('nvcc.exe')] + 'nvcc.exe')
                    install_flag = subprocess.call(((((((((((('"' + nvcc_path) + '"') + ' -o ') + '"') + compact_path) + '"') + ' --shared ') + '"') + compact_path[:(- 4)]) + '_win.cu') + '"'), shell=True)
            if (install_flag == 0):
                print('The model sampler has been installed successfully!')
        dll = ctypes.cdll.LoadLibrary(compact_path)
    elif (system_type == 'Linux'):
        compact_path = (os.path.dirname(__file__) + '/_compact/model_sampler.so')
        if (not os.path.exists(compact_path)):
            install_flag = subprocess.call((((((((('nvcc -Xcompiler -fPIC -shared -o ' + '"') + compact_path) + '"') + ' ') + '"') + compact_path[:(- 3)]) + '_linux.cu') + '"'), shell=True)
            if (install_flag != 0):
                search_flag = os.system('which nvcc')
                if (search_flag != 0):
                    Warning('Could not locate the path of nvcc, please make sure nvcc can be located by the system command "which nvcc"')
                else:
                    path_results = subprocess.check_output('which nvcc', shell=True)
                    path_results = str(path_results, encoding='utf8')
                    nvcc_path = path_results.split('\n')[0]
                    nvcc_path = (nvcc_path[:nvcc_path.find('nvcc')] + 'nvcc')
                    install_flag = subprocess.call(((((((((((('"' + nvcc_path) + '"') + ' -Xcompiler -fPIC -shared -o ') + '"') + compact_path) + '"') + ' ') + '"') + compact_path[:(- 3)]) + '_linux.cu') + '"'), shell=True)
            if (install_flag == 0):
                print('The model sampler has been installed successfully!')
        dll = ctypes.cdll.LoadLibrary(compact_path)
    self._init_status = dll._init_status
    self._init_status.argtypes = [ctypes.c_size_t]
    self._init_status.restype = ctypes.c_void_p
    self.rand_status = self._init_status(self.seed)
    self._multi_aug = dll._multi_aug
    self._multi_aug.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_void_p]
    self._crt_multi_aug = dll._crt_multi_aug
    self._crt_multi_aug.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_void_p]
    self._conv_multi_aug = dll._conv_multi_aug
    self._conv_multi_aug.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_void_p]
