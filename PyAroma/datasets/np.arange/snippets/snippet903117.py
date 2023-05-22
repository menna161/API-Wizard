from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import numpy as np
from .attack import Attack
from .utils import compute_success, get_labels_np_array, random_sphere, projection


def _minimal_perturbation(self, x, y):
    'Iteratively compute the minimal perturbation necessary to make the class prediction change. Stop when the\n        first adversarial example was found.\n\n        :param x: An array with the original inputs\n        :type x: `np.ndarray`\n        :param y:\n        :type y:\n        :return: An array holding the adversarial examples\n        :rtype: `np.ndarray`\n        '
    adv_x = x.copy()
    for batch_id in range(int(np.ceil((adv_x.shape[0] / float(self.batch_size))))):
        (batch_index_1, batch_index_2) = ((batch_id * self.batch_size), ((batch_id + 1) * self.batch_size))
        batch = adv_x[batch_index_1:batch_index_2]
        batch_labels = y[batch_index_1:batch_index_2]
        perturbation = self._compute_perturbation(batch, batch_labels)
        active_indices = np.arange(len(batch))
        current_eps = self.eps_step
        while ((active_indices.size > 0) and (current_eps <= self.eps)):
            current_x = self._apply_perturbation(x[batch_index_1:batch_index_2], perturbation, current_eps)
            batch[active_indices] = current_x[active_indices]
            adv_preds = self.classifier.predict(batch)
            if self.targeted:
                active_indices = np.where((np.argmax(batch_labels, axis=1) != np.argmax(adv_preds, axis=1)))[0]
            else:
                active_indices = np.where((np.argmax(batch_labels, axis=1) == np.argmax(adv_preds, axis=1)))[0]
            current_eps += self.eps_step
        adv_x[batch_index_1:batch_index_2] = batch
    return adv_x
