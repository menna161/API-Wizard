import torch
import numpy as np
from scipy.sparse import coo_matrix


def update(self, predictions, labels):
    'Updates the loss metric.'
    predictions = torch.argmax(predictions, dim=1)
    labels = labels.reshape([(- 1)]).cpu().numpy()
    predictions = predictions.reshape([(- 1)]).cpu().numpy()
    valid_labels = (labels >= 0)
    self.confusion_matrix += _compute_confusion_matrix(predictions[valid_labels], labels[valid_labels], self.num_classes)
