import argparse
import logging
import math
import os
import random
import sys
from typing import Callable, Optional
import numpy as np
import torch
from fairseq import checkpoint_utils, distributed_utils, options, quantization_utils, tasks, utils
from fairseq.data import iterators
from fairseq.logging import meters, metrics, progress_bar
from fairseq.model_parallel.megatron_trainer import MegatronTrainer
from fairseq.trainer import Trainer
import torch_xla.core.xla_model as xm
import torch_xla.distributed.parallel_loader as pl
import torch_xla.core.xla_model as xm
import torch_xla.distributed.xla_multiprocessing as xmp


def cli_main_helper(args):
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
        if (not getattr(args, 'tpu', False)):
            assert (args.distributed_world_size <= torch.cuda.device_count())
            port = random.randint(10000, 20000)
            args.distributed_init_method = 'tcp://localhost:{port}'.format(port=port)
            args.distributed_rank = None
            torch.multiprocessing.spawn(fn=distributed_main, args=(args,), nprocs=args.distributed_world_size)
        else:
            import torch_xla.distributed.xla_multiprocessing as xmp
            torch.multiprocessing.set_sharing_strategy('file_system')
            xmp.spawn(fn=distributed_main, args=(args,), nprocs=8)
    else:
        main(args)
