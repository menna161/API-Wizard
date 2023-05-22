import numpy as np
import mlopt.settings as stg


def accuracy(outputs, labels):
    '\n    Compute the accuracy, given the outputs and labels for all images.\n\n    Args:\n        outputs: (np.ndarray) output of the model\n        labels: (np.ndarray) batch labels\n\n    Returns: (float) accuracy in [0,1]\n    '
    outputs = np.argmax(outputs, axis=1)
    return (np.sum((outputs == labels)) / float(labels.size))
