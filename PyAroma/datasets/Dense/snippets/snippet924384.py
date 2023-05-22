from __future__ import print_function
from .net import Net
from .layers import *
from .bbdropout import BBDropout
from .misc import *


def __init__(self, n_classes, mask=None, name='vgg', reuse=None):
    super(VGG, self).__init__()
    n_units = [64, 64, 128, 128, 256, 256, 256, 512, 512, 512, 512, 512, 512, 512, 512]
    self.mask = mask
    self.n_classes = n_classes

    def create_block(l, n_in, n_out):
        self.base.append(Conv(n_in, n_out, 3, name=('conv' + str(l)), padding='SAME'))
        self.base.append(BatchNorm(n_out, name=('bn' + str(l))))
        self.bbd.append(BBDropout(n_out, name=('bbd' + str(l)), a_uc_init=2.0))
    with tf.variable_scope(name, reuse=reuse):
        create_block(1, 3, n_units[0])
        for i in range(1, 13):
            create_block((i + 1), n_units[(i - 1)], n_units[i])
        self.bbd.append(BBDropout(n_units[13], name='bbd14'))
        self.base.append(Dense(n_units[13], n_units[14], name='dense14'))
        self.base.append(BatchNorm(n_units[14], name='bn14'))
        self.bbd.append(BBDropout(n_units[14], name='bbd15'))
        self.base.append(Dense(n_units[14], n_classes, name='dense15'))
