import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L
from chainer_compiler.elichika import testtools


def forward(self, v1):
    return np.argmax(v1)
