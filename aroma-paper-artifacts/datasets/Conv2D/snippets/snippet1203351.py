import numpy as np
import pytest
import tinynn as tn


def test_conv_2d():
    batch_size = 1
    input_ = np.random.randn(batch_size, 16, 16, 1)
    layer = tn.layer.Conv2D(kernel=[4, 4, 1, 2], stride=[3, 3], padding='VALID')
    output = layer.forward(input_)
    assert (output.shape == (batch_size, 5, 5, 2))
    input_grads = layer.backward(output)
    assert (input_grads.shape == input_.shape)
    layer = tn.layer.Conv2D(kernel=[4, 4, 1, 2], stride=[3, 3], padding='SAME')
    output = layer.forward(input_)
    assert (output.shape == (batch_size, 6, 6, 2))
    input_grads = layer.backward(output)
    assert (input_grads.shape == input_.shape)
