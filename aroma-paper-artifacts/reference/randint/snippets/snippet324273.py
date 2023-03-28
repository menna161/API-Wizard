import os, sys, time, glob, random, argparse
import numpy as np, collections
from copy import deepcopy
import torch
import torch.nn as nn
from pathlib import Path
from config_utils import load_config, dict2config, configure2str
from datasets import get_datasets, SearchDataset
from procedures import prepare_seed, prepare_logger, save_checkpoint, copy_checkpoint, get_optim_scheduler
from utils import get_model_infos, obtain_accuracy
from log_utils import AverageMeter, time_string, convert_secs2time
from models import get_search_spaces, get_sub_search_spaces
from nas_102_api import NASBench102API as API
from R_EA import train_and_eval, random_architecture_func

if (__name__ == '__main__'):
    parser = argparse.ArgumentParser('Regularized Evolution Algorithm')
    parser.add_argument('--data_path', type=str, help='Path to dataset')
    parser.add_argument('--dataset', type=str, choices=['cifar10', 'cifar100', 'ImageNet16-120'], help='Choose between Cifar10/100 and ImageNet-16.')
    parser.add_argument('--search_space_name', type=str, help='The search space name.')
    parser.add_argument('--max_nodes', type=int, help='The maximum number of nodes.')
    parser.add_argument('--channel', type=int, help='The number of channels.')
    parser.add_argument('--num_cells', type=int, help='The number of cells in one stage.')
    parser.add_argument('--time_budget', type=int, help='The total time cost budge for searching (in seconds).')
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
        (save_dir, all_indexes, num) = (None, [], 500)
        for i in range(num):
            print('{:} : {:03d}/{:03d}'.format(time_string(), i, num))
            args.rand_seed = random.randint(1, 100000)
            (save_dir, index) = main(args, nas_bench)
            all_indexes.append(index)
        torch.save(all_indexes, (save_dir / 'results.pth'))
    else:
        main(args, nas_bench)
