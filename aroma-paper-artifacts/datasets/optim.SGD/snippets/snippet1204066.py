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


def benchmark_training(model, opts):
    'Benchmarks training phase.\n\n    :param obj model: A model to benchmark\n    :param dict opts: A dictionary of parameters.\n    :rtype: tuple:\n    :return: A tuple of (model_name, list of batch times)\n    '

    def _reduce_tensor(tensor):
        reduced = tensor.clone()
        dist.all_reduce(reduced, op=dist.reduce_op.SUM)
        reduced /= opts['world_size']
        return reduced
    if (opts['phase'] != 'training'):
        raise ("Phase in benchmark_training func is '%s'" % opts['phase'])
    opts['distributed'] = (opts['world_size'] > 1)
    opts['with_cuda'] = (opts['device'] == 'gpu')
    opts['fp16'] = (opts['dtype'] == 'float16')
    opts['loss_scale'] = 1
    if (opts['fp16'] and (not opts['with_cuda'])):
        raise ValueError('Configuration error: FP16 can only be used with GPUs')
    if opts['with_cuda']:
        torch.cuda.set_device(opts['local_rank'])
        cudnn.benchmark = opts['cudnn_benchmark']
        cudnn.fastest = opts['cudnn_fastest']
    if opts['distributed']:
        dist.init_process_group(backend=opts['dist_backend'], init_method='env://')
    if opts['with_cuda']:
        model = model.cuda()
        if (opts['dtype'] == 'float16'):
            model = network_to_half(model)
    if opts['distributed']:
        model = DDP(model, shared_param=True)
    if opts['fp16']:
        (model_params, master_params) = prep_param_lists(model)
    else:
        master_params = list(model.parameters())
    criterion = nn.CrossEntropyLoss()
    if opts['with_cuda']:
        criterion = criterion.cuda()
    optimizer = optim.SGD(master_params, lr=0.01, momentum=0.9, weight_decay=0.0001)
    data_loader = DatasetFactory.get_data_loader(opts, opts['__input_shape'], opts['__num_classes'])
    is_warmup = (opts['num_warmup_batches'] > 0)
    done = (opts['num_warmup_batches'] == 0)
    num_iterations_done = 0
    model.train()
    batch_times = np.zeros(opts['num_batches'])
    end_time = timeit.default_timer()
    while (not done):
        prefetcher = DataPrefetcher(data_loader, opts)
        (batch_data, batch_labels) = prefetcher.next()
        while (batch_data is not None):
            data_var = torch.autograd.Variable(batch_data)
            labels_var = torch.autograd.Variable(batch_labels)
            output = model(data_var)
            loss = criterion(output, labels_var)
            loss = (loss * opts['loss_scale'])
            if opts['fp16']:
                model.zero_grad()
                loss.backward()
                model_grads_to_master_grads(model_params, master_params)
                if (opts['loss_scale'] != 1):
                    for param in master_params:
                        param.grad.data = (param.grad.data / opts['loss_scale'])
                optimizer.step()
                master_params_to_model_params(model_params, master_params)
            else:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            if opts['with_cuda']:
                torch.cuda.synchronize()
            num_iterations_done += 1
            cur_time = timeit.default_timer()
            (batch_data, batch_labels) = prefetcher.next()
            if is_warmup:
                if (num_iterations_done >= opts['num_warmup_batches']):
                    is_warmup = False
                    num_iterations_done = 0
            else:
                if (opts['num_batches'] != 0):
                    batch_times[(num_iterations_done - 1)] = (cur_time - end_time)
                if (num_iterations_done >= opts['num_batches']):
                    done = True
                    break
            end_time = cur_time
    return (opts['__name'], batch_times)
