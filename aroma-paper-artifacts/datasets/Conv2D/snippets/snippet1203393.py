import numpy as np
import pytest
import tinynn as tn


@pytest.fixture(name='conv')
def fixture_conv_model():
    net = tn.net.Net([tn.layer.Conv2D(kernel=[3, 3, 1, 2]), tn.layer.MaxPool2D(pool_size=[2, 2], stride=[2, 2]), tn.layer.Conv2D(kernel=[3, 3, 2, 4]), tn.layer.MaxPool2D(pool_size=[2, 2], stride=[2, 2]), tn.layer.Flatten(), tn.layer.Dense(1)])
    loss = tn.loss.MSE()
    opt = tn.optimizer.SGD()
    return tn.model.Model(net, loss, opt)
