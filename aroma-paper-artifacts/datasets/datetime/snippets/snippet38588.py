import argparse
import datetime
import numpy
import chainer
from chainer.backends import cuda
import chainer.functions as F
import chainer.links as L
from chainer import training
from chainer.training import extensions
from testcases.ch2o_tests.utils import sequence_utils
from chainer_compiler import ch2o
import numpy as np


def forward(self, xs, h, c, mask):
    batch_size = len(xs)
    lens = [x.shape[0] for x in xs]
    max_len = self.sequence_length
    inputs = F.pad_sequence(xs)
    for time in range(max_len):
        x = inputs[(:, time)]
        input = F.concat((x, h), axis=1)
        gate = self.l(input)
        i = gate[(:, 0:self.num_hidden)]
        o = gate[(:, self.num_hidden:(self.num_hidden * 2))]
        f = gate[(:, (self.num_hidden * 2):(self.num_hidden * 3))]
        nc = gate[(:, (self.num_hidden * 3):(self.num_hidden * 4))]
        i = F.sigmoid(i)
        o = F.sigmoid(o)
        f = F.sigmoid(f)
        nc = F.tanh(nc)
        nc = ((f * c) + (i * nc))
        nh = (o * F.tanh(nc))
        m = mask[(:, time)]
        pmask = F.reshape(m, (self.batch_size,))
        pmask = F.broadcast_to(F.expand_dims(pmask, axis=1), (self.batch_size, self.num_hidden))
        nmask = (1.0 - pmask)
        h = ((nh * pmask) + (h * nmask))
    return h
