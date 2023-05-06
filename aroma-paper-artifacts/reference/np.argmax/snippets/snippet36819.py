import numpy as np
import tensorflow as tf
from .compute_overlap import compute_overlap
from .defaults import default_anchors_config


def compute_gt_annotations(anchors, annotations, negative_overlap=0.4, positive_overlap=0.5):
    ' Obtain indices of gt annotations with the greatest overlap.\n\tArgs\n\t\tanchors: np.array of annotations of shape (N, 4) for (x1, y1, x2, y2).\n\t\tannotations: np.array of shape (N, 5) for (x1, y1, x2, y2, label).\n\t\tnegative_overlap: IoU overlap for negative anchors (all anchors with overlap < negative_overlap are negative).\n\t\tpositive_overlap: IoU overlap or positive anchors (all anchors with overlap > positive_overlap are positive).\n\tReturns\n\t\tpositive_indices: indices of positive anchors\n\t\tignore_indices: indices of ignored anchors\n\t\targmax_overlaps_inds: ordered overlaps indices\n\t'
    overlaps = compute_overlap(anchors.astype(np.float64), annotations.astype(np.float64))
    argmax_overlaps_inds = np.argmax(overlaps, axis=1)
    max_overlaps = overlaps[(np.arange(overlaps.shape[0]), argmax_overlaps_inds)]
    positive_indices = (max_overlaps >= positive_overlap)
    ignore_indices = ((max_overlaps > negative_overlap) & (~ positive_indices))
    return (positive_indices, ignore_indices, argmax_overlaps_inds)
