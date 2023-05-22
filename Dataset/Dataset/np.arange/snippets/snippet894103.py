from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import random
import numpy as np


def begin(self, do_shuffle=True):
    'Move to the begin of the batch.'
    self.indices = np.arange(self.total(), dtype='int32')
    if do_shuffle:
        random.shuffle(self.indices)
    self.current_position = 0
    if ((self.current_position + self.minibatch_size) <= self.total()):
        self.current_batch_size = self.minibatch_size
    else:
        self.current_batch_size = (self.total() - self.current_position)
    self.current_batch_indices = self.indices[self.current_position:(self.current_position + self.current_batch_size)]
    self.current_input_length = max((self.data['clips'][(0, ind, 1)] for ind in self.current_batch_indices))
    self.current_output_length = max((self.data['clips'][(1, ind, 1)] for ind in self.current_batch_indices))
