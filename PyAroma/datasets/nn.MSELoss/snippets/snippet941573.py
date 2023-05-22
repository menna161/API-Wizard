import os
import tempfile
from unittest import TestCase
import torch
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras_adabound import AdaBound
from adabound import AdaBound as OfficialAdaBound


def test_same_amsgrad(self):
    self.reset_seed(51966)
    (w, b) = self.gen_random_weights()
    torch_linear = self.gen_torch_linear(w, b)
    keras_linear = self.gen_keras_linear(w, b, amsgrad=True)
    (w, b) = self.gen_random_weights()
    criterion = torch.nn.MSELoss()
    optimizer = OfficialAdaBound(torch_linear.parameters(), lr=0.001, final_lr=0.1, eps=K.epsilon(), amsbound=True)
    for i in range(300):
        x = np.random.standard_normal((1, 3))
        y = (np.dot(x, w) + b)
        optimizer.zero_grad()
        y_hat = torch_linear(torch.Tensor(x.tolist()))
        loss = criterion(y_hat, torch.Tensor(y.tolist()))
        torch_loss = loss.tolist()
        loss.backward()
        optimizer.step()
        keras_loss = keras_linear.train_on_batch(x, y)
    self.assertTrue((abs((torch_loss - keras_loss)) < 0.0001))
    self.assertTrue(np.allclose(torch_linear.weight.detach().numpy().transpose(), keras_linear.get_weights()[0], atol=0.0001))
    self.assertTrue(np.allclose(torch_linear.bias.detach().numpy(), keras_linear.get_weights()[1], atol=0.0001))
