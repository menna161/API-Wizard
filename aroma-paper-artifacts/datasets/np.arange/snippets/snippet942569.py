import numpy as np
from sklearn.metrics import pairwise_distances


def match_descriptors(descriptors1, descriptors2, cross_check=True, max_ratio=1.0):
    if (descriptors1.shape[1] != descriptors2.shape[1]):
        raise ValueError('Descriptor length must equal.')
    distances = pairwise_distances(descriptors1, descriptors2, n_jobs=(- 1))
    indices1 = np.arange(descriptors1.shape[0])
    indices2 = np.argmin(distances, axis=1)
    if cross_check:
        matches1 = np.argmin(distances, axis=0)
        mask = (indices1 == matches1[indices2])
        indices1 = indices1[mask]
        indices2 = indices2[mask]
    if (max_ratio < 1.0):
        distances = distances.astype(np.float64)
        best_distances = distances[(indices1, indices2)]
        distances[(indices1, indices2)] = np.inf
        second_best_indices2 = np.argmin(distances[indices1], axis=1)
        second_best_distances = distances[(indices1, second_best_indices2)]
        second_best_distances[(second_best_distances == 0)] = np.finfo(np.double).eps
        ratio = (best_distances / second_best_distances)
        mask = (ratio < max_ratio)
        indices1 = indices1[mask]
        indices2 = indices2[mask]
    matches = np.column_stack((indices1, indices2))
    return matches
