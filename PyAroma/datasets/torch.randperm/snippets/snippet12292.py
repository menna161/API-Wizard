import numpy as np
import torch
from FastAutoAugment.metrics import CrossEntropyLabelSmooth


def mixup(data, targets, alpha):
    indices = torch.randperm(data.size(0))
    shuffled_data = data[indices]
    shuffled_targets = targets[indices]
    lam = np.random.beta(alpha, alpha)
    lam = max(lam, (1.0 - lam))
    assert (0.0 <= lam <= 1.0), lam
    data = ((data * lam) + (shuffled_data * (1 - lam)))
    return (data, targets, shuffled_targets, lam)
