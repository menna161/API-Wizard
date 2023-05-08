import numpy as np
import datetime as dt
from lib.config import cfg
from lib.utils import weight_init
import torch.nn as nn


def __init__(self, random_seed=dt.datetime.now().microsecond, compute_grad=True):
    print('initializing "Net"')
    super(Net, self).__init__()
    self.rng = np.random.RandomState(random_seed)
    self.batch_size = cfg.CONST.BATCH_SIZE
    self.img_w = cfg.CONST.IMG_W
    self.img_h = cfg.CONST.IMG_H
    self.n_vox = cfg.CONST.N_VOX
    self.is_x_tensor4 = True
