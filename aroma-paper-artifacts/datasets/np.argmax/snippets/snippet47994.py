import torch
import numpy as np


def add(self, predicted, target):
    '\n        Computes the confusion matrix of K x K size where K is no of classes\n\n        Paramaters:\n            predicted (tensor): Can be an N x K tensor of predicted scores obtained from\n                the model for N examples and K classes or an N-tensor of\n                integer values between 0 and K-1.\n            target (tensor): Can be a N-tensor of integer values assumed to be integer\n                values between 0 and K-1 or N x K tensor, where targets are\n                assumed to be provided as one-hot vectors\n        '
    predicted = predicted.cpu().numpy()
    target = target.cpu().numpy()
    assert (predicted.shape[0] == target.shape[0]), 'number of targets and predicted outputs do not match'
    if (np.ndim(predicted) != 1):
        assert (predicted.shape[1] == self.k), 'number of predictions does not match size of confusion matrix'
        predicted = np.argmax(predicted, 1)
    else:
        assert ((predicted.max() < self.k) and (predicted.min() >= 0)), 'predicted values are not between 1 and k'
    onehot_target = (np.ndim(target) != 1)
    if onehot_target:
        assert (target.shape[1] == self.k), 'Onehot target does not match size of confusion matrix'
        assert ((target >= 0).all() and (target <= 1).all()), 'in one-hot encoding, target values should be 0 or 1'
        assert (target.sum(1) == 1).all(), 'multi-label setting is not supported'
        target = np.argmax(target, 1)
    else:
        assert ((predicted.max() < self.k) and (predicted.min() >= 0)), 'predicted values are not between 0 and k-1'
    x = (predicted + (self.k * target))
    bincount_2d = np.bincount(x.astype(np.int32), minlength=(self.k ** 2))
    assert (bincount_2d.size == (self.k ** 2))
    conf = bincount_2d.reshape((self.k, self.k))
    self.conf += conf
