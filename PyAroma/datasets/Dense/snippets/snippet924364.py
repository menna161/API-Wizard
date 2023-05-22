from .net import Net
from .layers import *
from .bbdropout import BBDropout


def __init__(self, n_units=None, mask=None, name='lenet_conv', reuse=None):
    n_units = ([20, 50, 800, 500] if (n_units is None) else n_units)
    self.mask = mask
    super(LeNetConv, self).__init__()
    with tf.variable_scope(name, reuse=reuse):
        self.base.append(Conv(1, n_units[0], 5, name='conv1'))
        self.base.append(Conv(n_units[0], n_units[1], 5, name='conv2'))
        self.base.append(Dense(n_units[2], n_units[3], name='dense3'))
        self.base.append(Dense(n_units[3], 10, name='dense4'))
        for i in range(4):
            self.bbd.append(BBDropout(n_units[i], name=('bbd' + str((i + 1)))))
