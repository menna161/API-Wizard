import argparse
from multiprocessing import Manager
import random
import unittest
import torch
import torch.nn as nn
from fairseq import distributed_utils, optim


def setup_args():
    args = argparse.Namespace()
    args.global_sync_iter = 20
    args.block_momentum = 0.875
    args.block_lr = 0.5
    args.input_size = 5
    args.nb_classes = 2
    args.batch_size = 1
    args.lr = [0.001]
    args.momentum = 0
    args.weight_decay = 0
    args.warmup_iterations = 0
    args.use_nbm = True
    args.average_sync = True
    args.global_sync_iter = 1
    args.model_parallel_size = 1
    args.distributed_backend = 'gloo'
    args.distributed_world_size = 2
    port = random.randint(10000, 20000)
    args.distributed_init_method = 'tcp://localhost:{port}'.format(port=port)
    args.distributed_init_host = 'localhost'
    args.distributed_port = (port + 1)
    args.local_world_size = args.distributed_world_size
    return args
