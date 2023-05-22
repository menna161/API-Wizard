import logging
import os
import pickle
import random
import socket
import struct
import subprocess
import warnings
from collections import OrderedDict
from typing import Any, Dict, Mapping
import torch
import torch.distributed as dist
from fairseq import utils
import torch_xla.core.xla_model as xm
import torch_xla.core.xla_model as xm
from fairseq.model_parallel.megatron.mpu import get_model_parallel_rank, initialize_model_parallel, model_parallel_cuda_manual_seed


def call_main(args, main, **kwargs):
    if (args.distributed_init_method is None):
        infer_init_method(args)
    if (args.distributed_init_method is not None):
        if ((torch.cuda.device_count() > 1) and (not args.distributed_no_spawn)):
            start_rank = args.distributed_rank
            args.distributed_rank = None
            kwargs['start_rank'] = start_rank
            torch.multiprocessing.spawn(fn=_distributed_main, args=(main, args, kwargs), nprocs=torch.cuda.device_count())
        else:
            _distributed_main(args.device_id, main, args, kwargs)
    elif (args.distributed_world_size > 1):
        assert (args.distributed_world_size <= torch.cuda.device_count())
        port = random.randint(10000, 20000)
        args.distributed_init_method = 'tcp://localhost:{port}'.format(port=port)
        args.distributed_rank = None
        torch.multiprocessing.spawn(fn=_distributed_main, args=(main, args, kwargs), nprocs=args.distributed_world_size)
    else:
        main(args, **kwargs)
