import collections
import math
import random
import numpy as np
import torch
from fairseq import checkpoint_utils, distributed_utils, options, progress_bar, tasks, utils
from fairseq.data import iterators
from fairseq.trainer import Trainer
from fairseq.meters import AverageMeter, StopwatchMeter


def cli_main():
    parser = options.get_training_parser()
    args = options.parse_args_and_arch(parser)
    if (args.distributed_init_method is None):
        distributed_utils.infer_init_method(args)
    if (args.distributed_init_method is not None):
        if ((torch.cuda.device_count() > 1) and (not args.distributed_no_spawn)):
            start_rank = args.distributed_rank
            args.distributed_rank = None
            torch.multiprocessing.spawn(fn=distributed_main, args=(args, start_rank), nprocs=torch.cuda.device_count())
        else:
            distributed_main(args.device_id, args)
    elif (args.distributed_world_size > 1):
        assert (args.distributed_world_size <= torch.cuda.device_count())
        port = random.randint(10000, 20000)
        args.distributed_init_method = 'tcp://localhost:{port}'.format(port=port)
        args.distributed_rank = None
        if ((max(args.update_freq) > 1) and (args.ddp_backend != 'no_c10d')):
            print('| NOTE: you may get better performance with: --ddp-backend=no_c10d')
        torch.multiprocessing.spawn(fn=distributed_main, args=(args,), nprocs=args.distributed_world_size)
    else:
        main(args)
