import numpy as np
import pytest
import tinynn as tn


@pytest.fixture(name='conv_model')
def fixture_conv_model():
    net = tn.net.Net([tn.layer.Conv2D(kernel=[3, 3, 1, 8], padding='VALID'), tn.layer.ReLU(), tn.layer.MaxPool2D(pool_size=[2, 2]), tn.layer.Conv2D(kernel=[3, 3, 8, 16], padding='VALID'), tn.layer.ReLU(), tn.layer.MaxPool2D(pool_size=[2, 2]), tn.layer.Flatten(), tn.layer.Dense(10)])
    loss = tn.loss.SoftmaxCrossEntropy()
    optimizer = tn.optimizer.Adam(0.001)
    return tn.model.Model(net=net, loss=loss, optimizer=optimizer)
