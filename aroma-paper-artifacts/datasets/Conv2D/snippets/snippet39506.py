from __future__ import division
import numpy as np
import chainer
import chainer.functions as F
from chainer import initializers
import chainer.links as L
from testcases.elichika_tests.chainercv_model.utils import Conv2DBNActiv
from testcases.elichika_tests.chainercv_model.resnet.resblock import ResBlock
from testcases.elichika_tests.chainercv_model.utils import PickableSequentialChain
from testcases.elichika_tests.chainercv_model.utils import prepare_pretrained_model
from chainer_compiler.elichika.parser import flags
from chainer_compiler.elichika import testtools
import numpy as np


def __init__(self, n_layer, n_class=None, pretrained_model=None, mean=None, initialW=None, fc_kwargs={}, arch='fb'):
    if (arch == 'fb'):
        stride_first = False
        conv1_no_bias = True
    elif (arch == 'he'):
        stride_first = True
        conv1_no_bias = (n_layer != 50)
    else:
        raise ValueError("arch is expected to be one of ['he', 'fb']")
    blocks = self._blocks[n_layer]
    (param, path) = prepare_pretrained_model({'n_class': n_class, 'mean': mean}, pretrained_model, self._models[arch][n_layer], {'n_class': 1000, 'mean': _imagenet_mean})
    self.mean = param['mean']
    if (initialW is None):
        initialW = initializers.HeNormal(scale=1.0, fan_option='fan_out')
    if ('initialW' not in fc_kwargs):
        fc_kwargs['initialW'] = initializers.Normal(scale=0.01)
    if pretrained_model:
        initialW = initializers.constant.Zero()
        fc_kwargs['initialW'] = initializers.constant.Zero()
    kwargs = {'initialW': initialW, 'stride_first': stride_first}
    super(ResNet, self).__init__()
    with self.init_scope():
        self.conv1 = Conv2DBNActiv(None, 64, 7, 2, 3, nobias=conv1_no_bias, initialW=initialW)
        self.pool1 = (lambda x: F.max_pooling_2d(x, ksize=3, stride=2))
        self.res2 = ResBlock(blocks[0], None, 64, 256, 1, **kwargs)
        self.res3 = ResBlock(blocks[1], None, 128, 512, 2, **kwargs)
        self.res4 = ResBlock(blocks[2], None, 256, 1024, 2, **kwargs)
        self.res5 = ResBlock(blocks[3], None, 512, 2048, 2, **kwargs)
        self.pool5 = (lambda x: F.average(x, axis=(2, 3)))
        self.fc6 = L.Linear(None, param['n_class'], **fc_kwargs)
        self.prob = F.softmax
        self._pick = ('prob',)
        self._return_tuple = False
    if path:
        chainer.serializers.load_npz(path, self)
