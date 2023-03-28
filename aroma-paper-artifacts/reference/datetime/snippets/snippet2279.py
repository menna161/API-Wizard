import numpy as np
import datetime as dt
import theano
import theano.tensor as tensor
from lib.config import cfg


def __init__(self, random_seed=dt.datetime.now().microsecond, compute_grad=True):
    self.rng = np.random.RandomState(random_seed)
    self.batch_size = cfg.CONST.BATCH_SIZE
    self.img_w = cfg.CONST.IMG_W
    self.img_h = cfg.CONST.IMG_H
    self.n_vox = cfg.CONST.N_VOX
    self.compute_grad = compute_grad
    self.x = tensor.tensor4()
    self.is_x_tensor4 = True
    self.y = tensor5()
    self.activations = []
    self.loss = []
    self.output = []
    self.error = []
    self.params = []
    self.grads = []
    self.setup()
