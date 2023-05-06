import numpy as np
import torch


def add(self, predicted, target):
    'Computes the confusion matrix\n\n        The shape of the confusion matrix is K x K, where K is the number\n        of classes.\n\n        Keyword arguments:\n        - predicted (Tensor or numpy.ndarray): Can be an N x K tensor/array of\n        predicted scores obtained from the model for N examples and K classes,\n        or an N-tensor/array of integer values between 0 and K-1.\n        - target (Tensor or numpy.ndarray): Can be an N x K tensor/array of\n        ground-truth classes for N examples and K classes, or an N-tensor/array\n        of integer values between 0 and K-1.\n\n        '
    (_, predicted) = predicted.max(1)
    predicted = predicted.view((- 1))
    target = target.view((- 1))
    if torch.is_tensor(predicted):
        predicted = predicted.cpu().numpy()
    if torch.is_tensor(target):
        target = target.cpu().numpy()
    assert (predicted.shape[0] == target.shape[0]), 'number of targets and predicted outputs do not match'
    if (np.ndim(predicted) != 1):
        assert (predicted.shape[1] == self.num_classes), 'number of predictions does not match size of confusion matrix'
        predicted = np.argmax(predicted, 1)
    else:
        assert ((predicted.max() < self.num_classes) and (predicted.min() >= 0)), 'predicted values are not between 0 and k-1'
    if (np.ndim(target) != 1):
        assert (target.shape[1] == self.num_classes), 'Onehot target does not match size of confusion matrix'
        assert ((target >= 0).all() and (target <= 1).all()), 'in one-hot encoding, target values should be 0 or 1'
        assert (target.sum(1) == 1).all(), 'multi-label setting is not supported'
        target = np.argmax(target, 1)
    else:
        assert ((target.max() < self.num_classes) and (target.min() >= 0)), 'target values are not between 0 and k-1'
    x = (predicted + (self.num_classes * target))
    bincount_2d = np.bincount(x.astype(np.int32), minlength=(self.num_classes ** 2))
    assert (bincount_2d.size == (self.num_classes ** 2))
    conf = bincount_2d.reshape((self.num_classes, self.num_classes))
    self.conf += conf
