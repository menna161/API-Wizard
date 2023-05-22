import gc
import datetime
import pynvml
import torch
import numpy as np


def track(self):
    '\n        Track the GPU memory usage\n        '
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(self.device)
    meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
    self.curr_line = self.frame.f_lineno
    where_str = (((((self.module_name + ' ') + self.func_name) + ':') + ' line ') + str(self.curr_line))
    with open(self.gpu_profile_fn, 'a+') as f:
        if self.begin:
            f.write(f'''GPU Memory Track | {datetime.datetime.now():%d-%b-%y-%H:%M:%S} | Total Used Memory:{(meminfo.used / (1000 ** 2)):<7.1f}Mb

''')
            self.begin = False
        if (self.print_detail is True):
            ts_list = [tensor.size() for tensor in self.get_tensors()]
            new_tensor_sizes = {(type(x), tuple(x.size()), ts_list.count(x.size()), ((np.prod(np.array(x.size())) * 4) / (1000 ** 2))) for x in self.get_tensors()}
            for (t, s, n, m) in (new_tensor_sizes - self.last_tensor_sizes):
                f.write(f'''+ | {str(n)} * Size:{str(s):<20} | Memory: {str((m * n))[:6]} M | {str(t):<20}
''')
            for (t, s, n, m) in (self.last_tensor_sizes - new_tensor_sizes):
                f.write(f'''- | {str(n)} * Size:{str(s):<20} | Memory: {str((m * n))[:6]} M | {str(t):<20} 
''')
            self.last_tensor_sizes = new_tensor_sizes
        f.write(f'''
At {where_str:<50}Total Used Memory:{(meminfo.used / (1000 ** 2)):<7.1f}Mb

''')
    pynvml.nvmlShutdown()
