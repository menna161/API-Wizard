import os
import numpy as np
import ctypes
import subprocess
from .pre_process import para_preprocess


def __init__(self, system_type='Windows', seed=0):
    '\n        The basic class for sampling distribution on cpu\n        '
    super(distribution_sampler_gpu, self).__init__()
    self.system_type = system_type
    self.seed = seed
    if (system_type == 'Windows'):
        '\n            To compile CUDA C/C++ under Windows system, Visual Studio and CUDA should have been installed.\n            This module has been tested under Visual Studio 2019(with MSVC v142 - VS 2019 C++ x64/x86 tools) and CUDA Toolkit 11.5.\n            '
        compact_path = (os.path.dirname(__file__) + '\\_compact\\distribution_sampler.dll')
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
                print('The distribution sampler has been installed successfully!')
        dll = ctypes.cdll.LoadLibrary(compact_path)
    elif (system_type == 'Linux'):
        compact_path = (os.path.dirname(__file__) + '/_compact/distribution_sampler.so')
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
                print('The distribution sampler has been installed successfully!')
        dll = ctypes.cdll.LoadLibrary(compact_path)
    self._init_status = dll._init_status
    self._init_status.argtypes = [ctypes.c_size_t]
    self._init_status.restype = ctypes.c_void_p
    self.rand_status = self._init_status(self.seed)
    self._sample_gamma = dll._sample_gamma
    self._sample_gamma.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_standard_gamma = dll._sample_standard_gamma
    self._sample_standard_gamma.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_beta = dll._sample_beta
    self._sample_beta.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_normal = dll._sample_normal
    self._sample_normal.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_standard_normal = dll._sample_standard_normal
    self._sample_standard_normal.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_void_p]
    self._sample_uniform = dll._sample_uniform
    self._sample_uniform.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_standard_uniform = dll._sample_standard_uniform
    self._sample_standard_uniform.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_void_p]
    self._sample_negative_binomial = dll._sample_negative_binomial
    self._sample_negative_binomial.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_multinomial = dll._sample_multinomial
    self._sample_multinomial.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_poisson = dll._sample_poisson
    self._sample_poisson.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_crt = dll._sample_crt
    self._sample_crt.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_cauchy = dll._sample_cauchy
    self._sample_cauchy.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_standard_cauchy = dll._sample_standard_cauchy
    self._sample_standard_cauchy.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_void_p]
    self._sample_chisquare = dll._sample_chisquare
    self._sample_chisquare.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_noncentral_chisquare = dll._sample_noncentral_chisquare
    self._sample_noncentral_chisquare.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_exponential = dll._sample_exponential
    self._sample_exponential.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_f = dll._sample_f
    self._sample_f.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_noncentral_f = dll._sample_noncentral_f
    self._sample_noncentral_f.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_geometric = dll._sample_geometric
    self._sample_geometric.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_gumbel = dll._sample_gumbel
    self._sample_gumbel.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_hypergeometric = dll._sample_hypergeometric
    self._sample_hypergeometric.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_laplace = dll._sample_laplace
    self._sample_laplace.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_logistic = dll._sample_logistic
    self._sample_logistic.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_power = dll._sample_power
    self._sample_power.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_zipf = dll._sample_zipf
    self._sample_zipf.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_pareto = dll._sample_pareto
    self._sample_pareto.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_rayleigh = dll._sample_rayleigh
    self._sample_rayleigh.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_t = dll._sample_t
    self._sample_t.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_triangular = dll._sample_triangular
    self._sample_triangular.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    self._sample_weibull = dll._sample_weibull
    self._sample_weibull.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
