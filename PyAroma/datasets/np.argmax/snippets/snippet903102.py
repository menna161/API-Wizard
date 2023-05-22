from __future__ import absolute_import, division, print_function, unicode_literals
import abc
import sys
import numpy as np
import logging as logger
import torch
import torch
import torch
import torch
import torch
import os
import torch
import time
import copy
import os
import torch
import torch.nn as nn
import torch.nn as nn
import torch.nn as nn


def loss_gradient(self, x, y, **kwargs):
    '\n        Compute the gradient of the loss function w.r.t. `x`.\n\n        :param x: Sample input with shape as expected by the model.\n        :type x: `np.ndarray`\n        :param y: Correct labels, one-vs-rest encoding.\n        :type y: `np.ndarray`\n        :return: Array of gradients of the same shape as `x`.\n        :rtype: `np.ndarray`\n        '
    import torch
    (x_preprocessed, y_preprocessed) = self._apply_preprocessing(x, y, fit=False)
    inputs_t = torch.from_numpy(x_preprocessed).to(self._device)
    inputs_t = inputs_t.float()
    inputs_t.requires_grad = True
    labels_t = torch.from_numpy(np.argmax(y_preprocessed, axis=1)).to(self._device)
    model_outputs = self._model(inputs_t)
    loss = self._loss(model_outputs[(- 1)], labels_t)
    self._model.zero_grad()
    loss.backward()
    grads = inputs_t.grad.cpu().numpy().copy()
    grads = self._apply_preprocessing_gradient(x, grads)
    assert (grads.shape == x.shape)
    return grads
