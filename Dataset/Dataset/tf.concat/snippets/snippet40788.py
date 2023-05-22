import tensorflow as tf
from tensorflow.contrib.rnn import RNNCell
from collections import namedtuple
from functools import reduce
from abc import abstractmethod
from typing import Tuple
from tacotron2.tacotron.modules import PreNet


def __call__(self, inputs, state: RNNStateHistoryWrapperState):
    (output, new_rnn_state) = self._cell(inputs, state.rnn_state)
    new_history = tf.concat([state.rnn_state_history, tf.expand_dims(output, axis=1)], axis=1)
    new_history.set_shape([None, None, self.output_size])
    new_state = RNNStateHistoryWrapperState(new_rnn_state, new_history, (state.time + 1))
    return (output, new_state)
