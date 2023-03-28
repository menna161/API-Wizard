from __future__ import print_function, division
import os
import argparse
import torch
import torch.multiprocessing as mp
from environment import create_env
from model import build_model
from train import train
from test import test
from shared_optim import SharedRMSprop, SharedAdam
import time
from datetime import datetime

if (__name__ == '__main__'):
    args = parser.parse_args()
    torch.manual_seed(args.seed)
    if (args.gpu_ids == (- 1)):
        torch.manual_seed(args.seed)
        args.gpu_ids = [(- 1)]
        device_share = torch.device('cpu')
    else:
        torch.cuda.manual_seed(args.seed)
        mp.set_start_method('spawn')
        if (len(args.gpu_ids) > 1):
            device_share = torch.device('cpu')
        else:
            device_share = torch.device(('cuda:' + str(args.gpu_ids[(- 1)])))
    env = create_env(args.env, args)
    shared_model = build_model(env.observation_space, env.action_space, args, device_share).to(device_share)
    if (args.train_mode == 0):
        params = shared_model.player0.parameters()
    elif (args.train_mode == 1):
        params = shared_model.player1.parameters()
    else:
        params = shared_model.parameters()
    if (args.load_model_dir is not None):
        saved_state = torch.load(args.load_model_dir, map_location=(lambda storage, loc: storage))
        shared_model.load_state_dict(saved_state)
    shared_model.share_memory()
    if args.shared_optimizer:
        if (args.optimizer == 'RMSprop'):
            optimizer = SharedRMSprop(params, lr=args.lr)
        if (args.optimizer == 'Adam'):
            optimizer = SharedAdam(params, lr=args.lr, amsgrad=args.amsgrad)
        optimizer.share_memory()
    else:
        optimizer = None
    current_time = datetime.now().strftime('%b%d_%H-%M')
    args.log_dir = os.path.join(args.log_dir, args.env, current_time)
    if (args.gpu_ids[(- 1)] == (- 1)):
        env.close()
    processes = []
    manager = mp.Manager()
    train_modes = manager.list()
    n_iters = manager.list()
    p = mp.Process(target=test, args=(args, shared_model, train_modes, n_iters))
    p.start()
    processes.append(p)
    time.sleep(args.sleep_time)
    for rank in range(0, args.workers):
        p = mp.Process(target=train, args=(rank, args, shared_model, optimizer, train_modes, n_iters))
        p.start()
        processes.append(p)
        time.sleep(args.sleep_time)
    for p in processes:
        time.sleep(args.sleep_time)
        p.join()
