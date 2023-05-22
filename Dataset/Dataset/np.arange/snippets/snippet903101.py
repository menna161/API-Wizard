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


def class_gradient(self, x, label=None, logits=False, **kwargs):
    '\n        Compute per-class derivatives w.r.t. `x`.\n\n        :param x: Sample input with shape as expected by the model.\n        :type x: `np.ndarray`\n        :param label: Index of a specific per-class derivative. If an integer is provided, the gradient of that class\n                      output is computed for all samples. If multiple values as provided, the first dimension should\n                      match the batch size of `x`, and each value will be used as target for its corresponding sample in\n                      `x`. If `None`, then gradients for all classes will be computed for each sample.\n        :type label: `int` or `list`\n        :param logits: `True` if the prediction should be done at the logits layer.\n        :type logits: `bool`\n        :return: Array of gradients of input features w.r.t. each class in the form\n                 `(batch_size, nb_classes, input_shape)` when computing for all classes, otherwise shape becomes\n                 `(batch_size, 1, input_shape)` when `label` parameter is specified.\n        :rtype: `np.ndarray`\n        '
    import torch
    if (not ((label is None) or (isinstance(label, (int, np.integer)) and (label in range(self._nb_classes))) or (isinstance(label, np.ndarray) and (len(label.shape) == 1) and (label < self._nb_classes).all() and (label.shape[0] == x.shape[0])))):
        raise ValueError(('Label %s is out of range.' % label))
    (x_preprocessed, _) = self._apply_preprocessing(x, y=None, fit=False)
    x_preprocessed = torch.from_numpy(x_preprocessed).to(self._device).float()
    if (self._layer_idx_gradients < 0):
        x_preprocessed.requires_grad = True
    model_outputs = self._model(x_preprocessed)
    if (self._layer_idx_gradients >= 0):
        input_grad = model_outputs[self._layer_idx_gradients]
    else:
        input_grad = x_preprocessed
    (logit_output, output) = (model_outputs[(- 2)], model_outputs[(- 1)])
    if logits:
        preds = logit_output
    else:
        preds = output
    grads = []

    def save_grad():

        def hook(grad):
            grads.append(grad.cpu().numpy().copy())
            grad.data.zero_()
        return hook
    input_grad.register_hook(save_grad())
    self._model.zero_grad()
    if (label is None):
        for i in range(self.nb_classes):
            torch.autograd.backward(preds[(:, i)], torch.Tensor(([1.0] * len(preds[(:, 0)]))).to(self._device), retain_graph=True)
    elif isinstance(label, (int, np.integer)):
        torch.autograd.backward(preds[(:, label)], torch.Tensor(([1.0] * len(preds[(:, 0)]))).to(self._device), retain_graph=True)
    else:
        unique_label = list(np.unique(label))
        for i in unique_label:
            torch.autograd.backward(preds[(:, i)], torch.Tensor(([1.0] * len(preds[(:, 0)]))).to(self._device), retain_graph=True)
        grads = np.swapaxes(np.array(grads), 0, 1)
        lst = [unique_label.index(i) for i in label]
        grads = grads[(np.arange(len(grads)), lst)]
        grads = grads[(None, ...)]
    grads = np.swapaxes(np.array(grads), 0, 1)
    grads = self._apply_preprocessing_gradient(x, grads)
    return grads
