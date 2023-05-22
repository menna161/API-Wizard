import datetime
import functools
import math
import os
import uuid
from torchvision import models
from advex_uar.attacks import PGDAttack, ElasticAttack, FrankWolfeAttack, JPEGAttack, GaborAttack, FogAttack, SnowAttack
from advex_uar.common.models import cifar10_resnet
from advex_uar.logging.logger import Logger


def init_logger(use_wandb, job_type, flags):
    if use_wandb:
        log_dir = None
        run_id = None
    else:
        dir_path = os.getcwd()
        time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        run_id = str(uuid.uuid4())[:8]
        dir_str = '{}-{}-{}'.format(job_type, time_str, run_id)
        log_dir = os.path.join(dir_path, job_type, dir_str)
        os.makedirs(log_dir, exist_ok=True)
    logger = Logger(use_wandb, job_type, run_id, log_dir=log_dir, flags=flags)
    return logger
