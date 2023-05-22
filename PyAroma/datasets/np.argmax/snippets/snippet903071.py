from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import numpy as np
from .attack import Attack
from .utils import compute_success, get_labels_np_array, tanh_to_original, original_to_tanh


def _loss_gradient(self, z_logits, target, x, x_adv, x_adv_tanh, c_weight, clip_min, clip_max):
    '\n        Compute the gradient of the loss function.\n\n        :param z_logits: An array with the current logits.\n        :type z_logits: `np.ndarray`\n        :param target: An array with the target class (one-hot encoded).\n        :type target: `np.ndarray`\n        :param x: An array with the original input.\n        :type x: `np.ndarray`\n        :param x_adv: An array with the adversarial input.\n        :type x_adv: `np.ndarray`\n        :param x_adv_tanh: An array with the adversarial input in tanh space.\n        :type x_adv_tanh: `np.ndarray`\n        :param c_weight: Weight of the loss term aiming for classification as target.\n        :type c_weight: `float`\n        :param clip_min: Minimum clipping value.\n        :type clip_min: `float`\n        :param clip_max: Maximum clipping value.\n        :type clip_max: `float`\n        :return: An array with the gradient of the loss function.\n        :type target: `np.ndarray`\n        '
    if self.targeted:
        i_sub = np.argmax(target, axis=1)
        i_add = np.argmax(((z_logits * (1 - target)) + ((np.min(z_logits, axis=1) - 1)[(:, np.newaxis)] * target)), axis=1)
    else:
        i_add = np.argmax(target, axis=1)
        i_sub = np.argmax(((z_logits * (1 - target)) + ((np.min(z_logits, axis=1) - 1)[(:, np.newaxis)] * target)), axis=1)
    loss_gradient = self.classifier.class_gradient(x_adv, label=i_add, logits=True)
    loss_gradient -= self.classifier.class_gradient(x_adv, label=i_sub, logits=True)
    loss_gradient = loss_gradient.reshape(x.shape)
    c_mult = c_weight
    for _ in range((len(x.shape) - 1)):
        c_mult = c_mult[(:, np.newaxis)]
    loss_gradient *= c_mult
    loss_gradient += (2 * (x_adv - x))
    loss_gradient *= (clip_max - clip_min)
    loss_gradient *= ((1 - np.square(np.tanh(x_adv_tanh))) / (2 * self._tanh_smoother))
    return loss_gradient
