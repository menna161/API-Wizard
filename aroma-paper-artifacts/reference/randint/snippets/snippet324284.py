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
from nas_102_api import NASBench102API as API
from models import CellStructure, get_search_spaces


def mutate_arch_func(parent_arch):
    child_arch = deepcopy(parent_arch)
    node_id = random.randint(0, (len(child_arch.nodes) - 1))
    node_info = list(child_arch.nodes[node_id])
    snode_id = random.randint(0, (len(node_info) - 1))
    xop = random.choice(op_names)
    while (xop == node_info[snode_id][0]):
        xop = random.choice(op_names)
    node_info[snode_id] = (xop, node_info[snode_id][1])
    child_arch.nodes[node_id] = tuple(node_info)
    return child_arch
