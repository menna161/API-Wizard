import os
import sys
import time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from super_model import SuperNetwork
from torch.autograd import Variable
from config import config
from test_server import TestClient
import copy
import functools
import pickle
import traceback


def get_mutation(self, k, mutation_num, m_prob):
    assert (k in self.keep_top_k)
    print('mutation ......')
    res = []
    iter = 0
    max_iters = (mutation_num * 10000)

    def random_func():
        cand = []
        if (len(self.keep_top_k[self.select_num]) > 0):
            cand = list(choice(self.keep_top_k[self.select_num]))
        for i in range(len(cand)):
            if (np.random.random_sample() < m_prob):
                k = np.random.randint(len(self.operations[i]))
                cand[i] = self.operations[i][k]
        return tuple(list(cand))
    cand_iter = self.stack_random_cand(random_func)
    while ((len(res) < mutation_num) and (max_iters > 0)):
        max_iters -= 1
        cand = next(cand_iter)
        if (not self.legal(cand)):
            continue
        res.append(cand)
        print('mutation {}/{} cand={}'.format(len(res), mutation_num, cand))
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('{} mutation_num = {}'.format(now, len(res)))
    return res
