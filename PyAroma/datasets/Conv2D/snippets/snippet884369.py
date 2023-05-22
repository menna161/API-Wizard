import sys
import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.layers import Lambda, Reshape, merge
from keras.models import Model
from ..utils import compose
from .keras_darknet19 import DarknetConv2D, DarknetConv2D_BN_Leaky, darknet_body
import tensorflow as tf


def yolo_loss(args, anchors, num_classes):
    'YOLO localization loss function.\n\n    Parameters\n    ----------\n    yolo_output : tensor\n        Final convolutional layer features.\n\n    true_boxes : tensor\n        Ground truth boxes tensor with shape [batch, num_true_boxes, 5]\n        containing box x_center, y_center, width, height, and class.\n\n    detectors_mask : array\n        0/1 mask for detector positions where there is a matching ground truth.\n\n    matching_true_boxes : array\n        Corresponding ground truth boxes for positive detector positions.\n        Already adjusted for conv height and width.\n\n    anchors : tensor\n        Anchor boxes for model.\n\n    num_classes : int\n        Number of object classes.\n\n    Returns\n    -------\n    mean_loss : float\n        mean localization loss across minibatch\n    '
    (yolo_output, true_boxes, detectors_mask, matching_true_boxes) = args
    num_anchors = len(anchors)
    object_scale = 5
    no_object_scale = 1
    class_scale = 1
    coordinates_scale = 1
    (pred_xy, pred_wh, pred_confidence, pred_class_prob) = yolo_head(yolo_output, anchors, num_classes)
    yolo_output_shape = K.shape(yolo_output)
    feats = K.reshape(yolo_output, [(- 1), yolo_output_shape[1], yolo_output_shape[2], num_anchors, (num_classes + 5)])
    pred_boxes = K.concatenate((K.sigmoid(feats[(..., 0:2)]), feats[(..., 2:4)]), axis=(- 1))
    pred_xy = K.expand_dims(pred_xy, 4)
    pred_wh = K.expand_dims(pred_wh, 4)
    pred_wh_half = (pred_wh / 2.0)
    pred_mins = (pred_xy - pred_wh_half)
    pred_maxes = (pred_xy + pred_wh_half)
    true_boxes_shape = K.shape(true_boxes)
    true_boxes = K.reshape(true_boxes, [true_boxes_shape[0], 1, 1, 1, true_boxes_shape[1], true_boxes_shape[2]])
    true_xy = true_boxes[(..., 0:2)]
    true_wh = true_boxes[(..., 2:4)]
    true_wh_half = (true_wh / 2.0)
    true_mins = (true_xy - true_wh_half)
    true_maxes = (true_xy + true_wh_half)
    intersect_mins = K.maximum(pred_mins, true_mins)
    intersect_maxes = K.minimum(pred_maxes, true_maxes)
    intersect_wh = K.maximum((intersect_maxes - intersect_mins), 0.0)
    intersect_areas = (intersect_wh[(..., 0)] * intersect_wh[(..., 1)])
    pred_areas = (pred_wh[(..., 0)] * pred_wh[(..., 1)])
    true_areas = (true_wh[(..., 0)] * true_wh[(..., 1)])
    union_areas = ((pred_areas + true_areas) - intersect_areas)
    iou_scores = (intersect_areas / union_areas)
    best_ious = K.max(iou_scores, axis=4)
    best_ious = K.expand_dims(best_ious)
    object_detections = K.cast((best_ious > 0.6), K.dtype(best_ious))
    no_object_weights = ((no_object_scale * (1 - object_detections)) * (1 - detectors_mask))
    no_objects_loss = (no_object_weights * K.square((- pred_confidence)))
    objects_loss = ((object_scale * detectors_mask) * K.square((1 - pred_confidence)))
    confidence_loss = (objects_loss + no_objects_loss)
    matching_classes = K.cast(matching_true_boxes[(..., 4)], 'int32')
    matching_classes = K.one_hot(matching_classes, num_classes)
    classification_loss = ((class_scale * detectors_mask) * K.square((matching_classes - pred_class_prob)))
    matching_boxes = matching_true_boxes[(..., 0:4)]
    coordinates_loss = ((coordinates_scale * detectors_mask) * K.square((matching_boxes - pred_boxes)))
    confidence_loss_sum = K.sum(confidence_loss)
    classification_loss_sum = K.sum(classification_loss)
    coordinates_loss_sum = K.sum(coordinates_loss)
    total_loss = (0.5 * ((confidence_loss_sum + classification_loss_sum) + coordinates_loss_sum))
    total_loss = tf.Print(total_loss, [total_loss, confidence_loss_sum, classification_loss_sum, coordinates_loss_sum], message='Total loss and components:')
    return total_loss
