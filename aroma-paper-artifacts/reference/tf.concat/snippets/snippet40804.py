import tensorflow as tf
from tensorflow.contrib.rnn import RNNCell
from collections import namedtuple
from functools import reduce
from abc import abstractmethod
from typing import Tuple
from tacotron2.tacotron.modules import PreNet


def call(self, inputs, state):
    (mgc_input, lf0_input) = inputs
    mgc_prenet_output = reduce((lambda acc, pn: pn(acc)), self.mgc_prenets, mgc_input)
    lf0_prenet_output = reduce((lambda acc, pn: pn(acc)), self.lf0_prenets, lf0_input)
    prenet_output = tf.concat([mgc_prenet_output, lf0_prenet_output], axis=(- 1))
    return self._cell(prenet_output, state)
