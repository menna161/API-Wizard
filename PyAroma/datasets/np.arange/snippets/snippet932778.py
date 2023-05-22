from __future__ import absolute_import
from collections import defaultdict
import numpy as np
from sklearn.metrics.base import _average_binary_score
from sklearn.metrics import precision_recall_curve, auc
from ..utils import to_numpy


def mean_ap(distmat, query_ids=None, gallery_ids=None, query_cams=None, gallery_cams=None):
    distmat = to_numpy(distmat)
    (m, n) = distmat.shape
    if (query_ids is None):
        query_ids = np.arange(m)
    if (gallery_ids is None):
        gallery_ids = np.arange(n)
    if (query_cams is None):
        query_cams = np.zeros(m).astype(np.int32)
    if (gallery_cams is None):
        gallery_cams = np.ones(n).astype(np.int32)
    query_ids = np.asarray(query_ids)
    gallery_ids = np.asarray(gallery_ids)
    query_cams = np.asarray(query_cams)
    gallery_cams = np.asarray(gallery_cams)
    indices = np.argsort(distmat, axis=1)
    matches = (gallery_ids[indices] == query_ids[(:, np.newaxis)])
    aps = []
    for i in range(m):
        valid = ((gallery_ids[indices[i]] != query_ids[i]) | (gallery_cams[indices[i]] != query_cams[i]))
        y_true = matches[(i, valid)]
        y_score = (- distmat[i][indices[i]][valid])
        if (not np.any(y_true)):
            continue
        aps.append(average_precision_score(y_true, y_score))
    if (len(aps) == 0):
        raise RuntimeError('No valid query')
    return np.mean(aps)
