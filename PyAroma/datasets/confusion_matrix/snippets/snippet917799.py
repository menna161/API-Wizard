import numpy as np
from medpy import metric


def hausdorff_distance(test=None, reference=None, confusion_matrix=None, nan_for_nonexisting=True, voxel_spacing=None, connectivity=1, **kwargs):
    if (confusion_matrix is None):
        confusion_matrix = ConfusionMatrix(test, reference)
    (test_empty, test_full, reference_empty, reference_full) = confusion_matrix.get_existence()
    if (test_empty or test_full or reference_empty or reference_full):
        if nan_for_nonexisting:
            return float('NaN')
        else:
            return 0
    (test, reference) = (confusion_matrix.test, confusion_matrix.reference)
    return metric.hd(test, reference, voxel_spacing, connectivity)
