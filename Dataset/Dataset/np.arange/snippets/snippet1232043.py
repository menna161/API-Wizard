import operator as op
from typing import Union, Tuple
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable


def _compensate_confidence(self, outputs, targets):
    '\n        Compensate for ``self.confidence`` and returns a new weighted sum\n        vector.\n\n        :param outputs: the weighted sum right before the last layer softmax\n               normalization, of dimension [B x M]\n        :type outputs: np.ndarray\n        :param targets: either the attack targets or the real image labels,\n               depending on whether or not ``self.targeted``, of dimension [B]\n        :type targets: np.ndarray\n        :return: the compensated weighted sum of dimension [B x M]\n        :rtype: np.ndarray\n        '
    outputs_comp = np.copy(outputs)
    rng = np.arange(targets.shape[0])
    if self.targeted:
        outputs_comp[(rng, targets)] -= self.confidence
    else:
        outputs_comp[(rng, targets)] += self.confidence
    return outputs_comp
