import chainer
from chainer.functions import relu
from chainer.links import Convolution2D
from chainer.links import DilatedConvolution2D


def __init__(self, in_channels, out_channels, ksize=None, stride=1, pad=0, dilate=1, nobias=False, initialW=None, initial_bias=None, activ=relu):
    if (ksize is None):
        (out_channels, ksize, in_channels) = (in_channels, out_channels, None)
    self.activ = activ
    super(Conv2DActiv, self).__init__()
    with self.init_scope():
        if (dilate > 1):
            self.conv = DilatedConvolution2D(in_channels, out_channels, ksize, stride, pad, dilate, nobias, initialW, initial_bias)
        else:
            self.conv = Convolution2D(in_channels, out_channels, ksize, stride, pad, nobias, initialW, initial_bias)
