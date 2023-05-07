import numpy as np
import tensorflow as tf
from .compute_overlap import compute_overlap
from .defaults import default_anchors_config


def shift(image_shape, features_shape, stride, anchors):
    ' Produce shifted anchors based on shape of the image, shape of the feature map and stride.\n\tArgs\n\t\timage_shape   : Shape of the input image.\n\t\tfeatures_shape: Shape of the feature map.\n\t\tstride        : Stride to shift the anchors with over the shape.\n\t\tanchors       : The anchors to apply at each location.\n\t'
    offset_x = ((image_shape[1] - ((features_shape[1] - 1) * stride)) / 2.0)
    offset_y = ((image_shape[0] - ((features_shape[0] - 1) * stride)) / 2.0)
    shift_x = ((np.arange(0, features_shape[1]) * stride) + offset_x)
    shift_y = ((np.arange(0, features_shape[0]) * stride) + offset_y)
    (shift_x, shift_y) = np.meshgrid(shift_x, shift_y)
    shifts = np.vstack((shift_x.ravel(), shift_y.ravel(), shift_x.ravel(), shift_y.ravel())).transpose()
    A = anchors.shape[0]
    K = shifts.shape[0]
    all_anchors = (anchors.reshape((1, A, 4)) + shifts.reshape((1, K, 4)).transpose((1, 0, 2)))
    all_anchors = all_anchors.reshape(((K * A), 4))
    return all_anchors
