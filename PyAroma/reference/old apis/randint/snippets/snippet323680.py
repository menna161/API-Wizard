import os, sys, time, glob, random, argparse
import numpy as np, collections
from copy import deepcopy
from pathlib import Path
import torch
import torch.nn as nn
from config_utils import load_config, dict2config, configure2str
from datasets import get_datasets, SearchDataset
from procedures import prepare_seed, prepare_logger, save_checkpoint, copy_checkpoint, get_optim_scheduler
from utils import get_model_infos, obtain_accuracy
from log_utils import AverageMeter, time_string, convert_secs2time
from nas_102_api import NASBench102API as API
from models import CellStructure, get_search_spaces
import ConfigSpace
from hpbandster.optimizers.bohb import BOHB
import hpbandster.core.nameserver as hpns
from hpbandster.core.worker import Worker

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser('Regularized Evolution Algorithm')
    parser.add_argument('--data_path', type=str, help='Path to dataset')
    parser.add_argument('--dataset', type=str, choices=['cifar10', 'cifar100', 'ImageNet16-120'], help='Choose between Cifar10/100 and ImageNet-16.')
    parser.add_argument('--search_space_name', type=str, help='The search space name.')
    parser.add_argument('--max_nodes', type=int, help='The maximum number of nodes.')
    parser.add_argument('--channel', type=int, help='The number of channels.')
    parser.add_argument('--num_cells', type=int, help='The number of cells in one stage.')
    parser.add_argument('--time_budget', type=int, help='The total time cost budge for searching (in seconds).')
    parser.add_argument('--strategy', default='sampling', type=str, nargs='?', help='optimization strategy for the acquisition function')
    parser.add_argument('--min_bandwidth', default=0.3, type=float, nargs='?', help='minimum bandwidth for KDE')
    parser.add_argument('--num_samples', default=64, type=int, nargs='?', help='number of samples for the acquisition function')
    parser.add_argument('--random_fraction', default=0.33, type=float, nargs='?', help='fraction of random configurations')
    parser.add_argument('--bandwidth_factor', default=3, type=int, nargs='?', help='factor multiplied to the bandwidth')
    parser.add_argument('--n_iters', default=100, type=int, nargs='?', help='number of iterations for optimization method')
    parser.add_argument('--workers', type=int, default=2, help='number of data loading workers (default: 2)')
    parser.add_argument('--save_dir', type=str, help='Folder to save checkpoints and log.')
    parser.add_argument('--arch_nas_dataset', type=str, help='The path to load the architecture dataset (tiny-nas-benchmark).')
    parser.add_argument('--print_freq', type=int, help='print frequency (default: 200)')
    parser.add_argument('--rand_seed', type=int, help='manual seed')
    args = parser.parse_args()
    if ((args.arch_nas_dataset is None) or (not os.path.isfile(args.arch_nas_dataset))):
        nas_bench = None
    else:
        print('{:} build NAS-Benchmark-API from {:}'.format(time_string(), args.arch_nas_dataset))
        nas_bench = API(args.arch_nas_dataset)
    if (args.rand_seed < 0):
        (save_dir, all_indexes, num, all_times) = (None, [], 500, [])
        for i in range(num):
            print('{:} : {:03d}/{:03d}'.format(time_string(), i, num))
            args.rand_seed = random.randint(1, 100000)
            (save_dir, index, ctime) = main(args, nas_bench)
            all_indexes.append(index)
            all_times.append(ctime)
        print('\n average time : {:.3f} s'.format((sum(all_times) / len(all_times))))
        torch.save(all_indexes, (save_dir / 'results.pth'))
    else:
        main(args, nas_bench)
