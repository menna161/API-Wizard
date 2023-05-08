import collections
import datetime
import importlib
import math
import os.path
import pprint
import random
import subprocess
import sys
import git
import numpy as np
import sacred
import tensorboardX
import torch
import tqdm


def sacred_main_helper(train_func, args, _run):
    '\n    Helper function\n    '
    for (k, v) in args.__dict__.items():
        if (type(v) == sacred.config.custom_containers.ReadOnlyList):
            setattr(args, k, list(v))
    args.experiment_name = experiment_name(args)
    repo = git.Repo('../..')
    args.git_clean = (not repo.is_dirty())
    if ((not args.git_clean) and args.require_clean_repo):
        raise RuntimeError('The repo is not clean, change require_clean_repo flag if you want torun the code with a dirty repo.')
    args.git_commit = git_revision()
    args.cuda = ((not args.no_cuda) and torch.cuda.is_available())
    torch.set_default_tensor_type(('torch.cuda.FloatTensor' if args.cuda else 'torch.FloatTensor'))
    args.device = ('cuda' if args.cuda else 'cpu')
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    args.runid = ((datetime.datetime.now().strftime('%y%m%d_%H%M_%f') + '_') + args.git_commit)
    if (args.logs_root is None):
        args.logs_root = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), '../../logs'))
    args.output_folder = os.path.join(args.logs_root, f'{args.experiment_name}_{args.runid}')
    os.mkdir(args.output_folder)
    _run.info['output_folder'] = os.path.abspath(args.output_folder)
    _run.info['args'] = args.__dict__
    _writer = tensorboardX.SummaryWriter(os.path.join(args.output_folder, 'tensorboard.file'))
    _writer.add_text('hyperparameters', pprint.pformat(args.__dict__))
    with open(os.path.join(args.output_folder, 'config.txt'), 'wt') as out:
        pprint.pprint(args.__dict__, stream=out)
    pprint.pprint(args.__dict__)
    return train_func(args, _run, _writer)
