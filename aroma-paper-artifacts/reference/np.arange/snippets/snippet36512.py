import numpy as np


def get_sub_slice(indices, sub_indices):
    '\n    Safe indexer with nested slices.\n\n    Parameters\n    ----------\n    indices: ndarray or slice\n    sub_indices: ndarray or slice\n\n    Returns\n    -------\n    result: np.array(indices[sub_indices])\n    '
    if (indices is None):
        if isinstance(sub_indices, slice):
            return np.arange(sub_indices.start, sub_indices.stop)
        else:
            return sub_indices
    elif isinstance(indices, slice):
        return np.arange((indices.start + sub_indices.start), (indices.start + sub_indices.stop))
    else:
        return indices[sub_indices]
