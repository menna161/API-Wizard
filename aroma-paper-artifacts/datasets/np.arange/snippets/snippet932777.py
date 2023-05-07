from __future__ import absolute_import
from collections import defaultdict
import numpy as np
from sklearn.metrics.base import _average_binary_score
from sklearn.metrics import precision_recall_curve, auc
from ..utils import to_numpy


def cmc(distmat, query_ids=None, gallery_ids=None, query_cams=None, gallery_cams=None, topk=100, separate_camera_set=False, single_gallery_shot=False, first_match_break=False):
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
    ret = np.zeros(topk)
    num_valid_queries = 0
    for i in range(m):
        valid = ((gallery_ids[indices[i]] != query_ids[i]) | (gallery_cams[indices[i]] != query_cams[i]))
        if separate_camera_set:
            valid &= (gallery_cams[indices[i]] != query_cams[i])
        if (not np.any(matches[(i, valid)])):
            continue
        if single_gallery_shot:
            repeat = 10
            gids = gallery_ids[indices[i][valid]]
            inds = np.where(valid)[0]
            ids_dict = defaultdict(list)
            for (j, x) in zip(inds, gids):
                ids_dict[x].append(j)
        else:
            repeat = 1
        for _ in range(repeat):
            if single_gallery_shot:
                sampled = (valid & _unique_sample(ids_dict, len(valid)))
                index = np.nonzero(matches[(i, sampled)])[0]
            else:
                index = np.nonzero(matches[(i, valid)])[0]
            delta = (1.0 / (len(index) * repeat))
            for (j, k) in enumerate(index):
                if ((k - j) >= topk):
                    break
                if first_match_break:
                    ret[(k - j)] += 1
                    break
                ret[(k - j)] += delta
        num_valid_queries += 1
    if (num_valid_queries == 0):
        raise RuntimeError('No valid query')
    return (ret.cumsum() / num_valid_queries)
