import chainer
from chainer.functions import relu
from chainer.links import BatchNormalization
from chainer.links import Convolution2D
from chainer_compiler.elichika.parser import flags
from chainermn.links import MultiNodeBatchNormalization


def __init__(self, in_channels, out_channels, ksize=None, stride=1, pad=0, dilate=1, groups=1, nobias=True, initialW=None, initial_bias=None, activ=relu, bn_kwargs={}):
    if (ksize is None):
        (out_channels, ksize, in_channels) = (in_channels, out_channels, None)
    self.activ = activ
    super(Conv2DBNActiv, self).__init__()
    with self.init_scope():
        self.conv = Convolution2D(in_channels, out_channels, ksize, stride, pad, nobias, initialW, initial_bias, dilate=dilate, groups=groups)
        if ('comm' in bn_kwargs):
            with flags.ignore_branch():
                self.bn = MultiNodeBatchNormalization(out_channels, **bn_kwargs)
        else:
            self.bn = BatchNormalization(out_channels, **bn_kwargs)
