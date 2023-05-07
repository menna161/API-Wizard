import argparse
import datetime
import logging
import numpy as np
import chainer
from chainer.backends import cuda
import chainer.functions as F
import chainer.links as L
from chainer import training
from chainer.training import extensions
from testcases.ch2o_tests.utils import sequence_utils
from chainer_compiler import ch2o
import numpy as np


def forward(self, xs, ilens):
    'VGG2L forward\n\n        :param xs:\n        :param ilens:\n        :return:\n        '
    logging.info(((self.__class__.__name__ + ' input lengths: ') + str(ilens)))
    xs = F.pad_sequence(xs)
    xs = F.swapaxes(F.reshape(xs, (xs.shape[0], xs.shape[1], self.in_channel, (xs.shape[2] // self.in_channel))), 1, 2)
    xs = F.relu(self.conv1_1(xs))
    xs = F.relu(self.conv1_2(xs))
    xs = F.max_pooling_2d(xs, 2, stride=2)
    xs = F.relu(self.conv2_1(xs))
    xs = F.relu(self.conv2_2(xs))
    xs = F.max_pooling_2d(xs, 2, stride=2)
    ilens = ((ilens + 1) // 2)
    ilens = ((ilens + 1) // 2)
    xs = F.swapaxes(xs, 1, 2)
    xs = F.reshape(xs, (xs.shape[0], xs.shape[1], (xs.shape[2] * xs.shape[3])))
    xs = [xs[(i, :ilens[i], :)] for i in range(len(ilens))]
    return (xs, ilens)
