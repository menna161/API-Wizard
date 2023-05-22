from __future__ import absolute_import
from __future__ import print_function
import sys
import os
import traceback
import argparse
import timeit
import json
import numpy as np
import torch
import torch.nn as nn
import torch.distributed as dist
import torch.autograd as autograd
import torch.optim as optim
import torch.backends.cudnn as cudnn
from pytorch_benchmarks.model_factory import ModelFactory
from pytorch_benchmarks.dataset_factory import DatasetFactory, DataPrefetcher
from apex.parallel import DistributedDataParallel as DDP
from apex.fp16_utils import network_to_half, prep_param_lists, model_grads_to_master_grads, master_params_to_model_params


def benchmark_inference(model, opts):
    'Benchmarks inference phase.\n\n    :param obj model: A model to benchmark\n    :param dict opts: A dictionary of parameters.\n    :rtype: tuple\n    :return: A tuple of (model_name, list of batch times)\n    '
    if (opts['phase'] != 'inference'):
        raise ("Phase in benchmark_inference func is '%s'" % opts['phase'])
    if ((opts['device'] == 'gpu') and (opts['world_size'] != 1)):
        raise ('GPU inference can only be used with one GPU (world_size: %d).' % opts['world_size'])
    data = autograd.Variable(torch.randn(((opts['batch_size'],) + model.input_shape)))
    if (opts['device'] == 'gpu'):
        cudnn.benchmark = opts['cudnn_benchmark']
        cudnn.fastest = opts['cudnn_fastest']
        data = data.cuda()
        model = model.cuda()
    if (opts['dtype'] == 'float16'):
        data = data.half()
        model = model.half()
    model.eval()
    for i in range(opts['num_warmup_batches']):
        model(data)
    batch_times = np.zeros(opts['num_batches'])
    for i in range(opts['num_batches']):
        start_time = timeit.default_timer()
        model(data)
        batch_times[i] = (timeit.default_timer() - start_time)
    return (model.name, batch_times)
