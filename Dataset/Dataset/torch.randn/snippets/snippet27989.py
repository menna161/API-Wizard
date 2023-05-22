import os
import hydra
import hydra.experimental
import numpy as np
import pytest
import torch


@pytest.helpers.register
def semseg_test(model):
    (B, N) = (4, 2048)
    inputs = torch.randn(B, N, 9).cuda()
    labels = torch.from_numpy(np.random.randint(0, 3, size=(B * N))).view(B, N).cuda()
    model.cuda()
    _test_loop(model, inputs, labels)
