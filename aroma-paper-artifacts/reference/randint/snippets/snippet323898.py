import os, sys, time, glob, random, argparse
import numpy as np
from copy import deepcopy
import torch
import torch.nn as nn
from pathlib import Path
from config_utils import load_config, dict2config, configure2str
from datasets import get_datasets, get_nas_search_loaders
from procedures import prepare_seed, prepare_logger, save_checkpoint, copy_checkpoint, get_optim_scheduler
from utils import get_model_infos, obtain_accuracy
from log_utils import AverageMeter, time_string, convert_secs2time
from models import get_cell_based_tiny_net, get_search_spaces, OPS_CODING
from nas_102_api import NASBench102API as API
import pdb
import time
import scipy
import scipy.stats
from weight_angle import get_arch_angle

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser('SETN')
    parser.add_argument('--data_path', type=str, help='Path to dataset')
    parser.add_argument('--dataset', type=str, choices=['cifar10', 'cifar100', 'ImageNet16-120'], help='Choose between Cifar10/100 and ImageNet-16.')
    parser.add_argument('--search_space_name', type=str, help='The search space name.')
    parser.add_argument('--max_nodes', type=int, help='The maximum number of nodes.')
    parser.add_argument('--channel', type=int, help='The number of channels.')
    parser.add_argument('--num_cells', type=int, help='The number of cells in one stage.')
    parser.add_argument('--select_num', type=int, help='The number of selected architectures to evaluate.')
    parser.add_argument('--track_running_stats', type=int, choices=[0, 1], help='Whether use track_running_stats or not in the BN layer.')
    parser.add_argument('--config_path', type=str, help='The path of the configuration.')
    parser.add_argument('--arch_learning_rate', type=float, default=0.0003, help='learning rate for arch encoding')
    parser.add_argument('--arch_weight_decay', type=float, default=0.001, help='weight decay for arch encoding')
    parser.add_argument('--workers', type=int, default=2, help='number of data loading workers (default: 2)')
    parser.add_argument('--save_dir', type=str, help='Folder to save checkpoints and log.')
    parser.add_argument('--arch_nas_dataset', type=str, help='The path to load the architecture dataset (tiny-nas-benchmark).')
    parser.add_argument('--print_freq', type=int, help='print frequency (default: 200)')
    parser.add_argument('--rand_seed', type=int, help='manual seed')
    args = parser.parse_args()
    if ((args.rand_seed is None) or (args.rand_seed < 0)):
        args.rand_seed = random.randint(1, 100000)
    main(args)
