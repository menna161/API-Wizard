import numpy
import chainer
import chainer.functions as F
import chainer.links as L
from chainer_compiler.elichika import testtools
import numpy as np


def main():
    np.random.seed(314)
    batch_size = 3
    num_hidden = 5
    sequence_length = 4
    model = LinkInFor(num_hidden)
    x = np.random.rand(batch_size, sequence_length, num_hidden).astype(np.float32)
    h = np.random.rand(batch_size, num_hidden).astype(np.float32)
    args = [x, h, np.arange(sequence_length)]
    testtools.generate_testcase(model, args)
