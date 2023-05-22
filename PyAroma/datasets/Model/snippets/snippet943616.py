import argparse
from multiprocessing import Manager
import random
import unittest
import torch
import torch.nn as nn
from fairseq import distributed_utils, optim


def setup_model_loss_criterion(args, rank, is_cuda):
    '\n    setup model, criterion and optimizer based on input args\n    '
    args.distributed_rank = rank
    if (args.distributed_world_size > 1):
        distributed_utils.distributed_init(args)
    torch.manual_seed(1)
    model = Model(args.input_size, args.nb_classes)
    loss_fn = nn.CrossEntropyLoss()
    if is_cuda:
        model = model.cuda()
        loss_fn = loss_fn.cuda()
    optimizer = optim.sgd.SGD(args, model.parameters())
    optimizer = optim.FairseqBMUF(args, optimizer)
    return (model, loss_fn, optimizer)
