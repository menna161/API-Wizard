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

if (__name__ == '__main__'):
    import numpy as np
    np.random.seed(314)
    batch_size = 3
    sequence_length = 4
    num_vocabs = 10
    num_hidden = 5
    model_fn = (lambda : MyLSTM(num_hidden, batch_size, sequence_length))
    (labels, lengths) = sequence_utils.gen_random_sequence(batch_size, sequence_length, num_vocabs)
    xs = []
    for l in lengths:
        xs.append(np.random.rand(l, num_hidden).astype(dtype=np.float32))
    h = np.zeros((batch_size, num_hidden), dtype=np.float32)
    c = np.zeros((batch_size, num_hidden), dtype=np.float32)
    mask = (np.expand_dims(np.arange(sequence_length), 0) < np.expand_dims(lengths, 1)).astype(np.float32)
    args = [xs, h, c, mask]
    ch2o.generate_testcase(model_fn, args)
