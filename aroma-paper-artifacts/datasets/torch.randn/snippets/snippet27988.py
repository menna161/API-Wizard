import os
import hydra
import hydra.experimental
import numpy as np
import pytest
import torch


@pytest.helpers.register
def cls_test(model):
    (B, N) = (4, 2048)
    inputs = torch.randn(B, N, 6).cuda()
    labels = torch.from_numpy(np.random.randint(0, 3, size=B)).cuda()
    model.cuda()
    _test_loop(model, inputs, labels)
