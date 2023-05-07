import logging
import os
from datetime import datetime
from pathlib import Path
import torch
from classy_vision.generic.distributed_util import get_rank, get_world_size
from classy_vision.generic.opts import check_generic_args, parse_train_arguments
from classy_vision.generic.registry_utils import import_all_packages_from_directory
from classy_vision.generic.util import load_checkpoint, load_json
from classy_vision.hooks import CheckpointHook, LossLrMeterLoggingHook, ModelComplexityHook, ProfilerHook, ProgressBarHook, TensorboardPlotHook, VisdomHook
from classy_vision.tasks import FineTuningTask, build_task
from classy_vision.trainer import DistributedTrainer, LocalTrainer
from torchvision import set_image_backend, set_video_backend
from torch.utils.tensorboard import SummaryWriter


def configure_hooks(args, config):
    hooks = [LossLrMeterLoggingHook(args.log_freq), ModelComplexityHook()]
    suffix = datetime.now().isoformat()
    base_folder = f'{Path(__file__).parent}/output_{suffix}'
    if (args.checkpoint_folder == ''):
        args.checkpoint_folder = (base_folder + '/checkpoints')
        os.makedirs(args.checkpoint_folder, exist_ok=True)
    logging.info(f'Logging outputs to {base_folder}')
    logging.info(f'Logging checkpoints to {args.checkpoint_folder}')
    if (not args.skip_tensorboard):
        try:
            from torch.utils.tensorboard import SummaryWriter
            tb_writer = SummaryWriter(log_dir=(Path(base_folder) / 'tensorboard'))
            hooks.append(TensorboardPlotHook(tb_writer))
        except ImportError:
            logging.warning('tensorboard not installed, skipping tensorboard hooks')
    args_dict = vars(args)
    args_dict['config'] = config
    hooks.append(CheckpointHook(args.checkpoint_folder, args_dict, checkpoint_period=args.checkpoint_period))
    if args.profiler:
        hooks.append(ProfilerHook())
    if args.show_progress:
        hooks.append(ProgressBarHook())
    if (args.visdom_server != ''):
        hooks.append(VisdomHook(args.visdom_server, args.visdom_port))
    return hooks
