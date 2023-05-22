from functools import wraps
import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.engine.base_layer import Layer
from keras.layers import Conv2D, Add, ZeroPadding2D, UpSampling2D, Concatenate, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.normalization import BatchNormalization
from keras.models import Model
from keras.regularizers import l2
from yolo4.utils import compose


def yolo4_loss(args, anchors, num_classes, ignore_thresh=0.5, label_smoothing=0, use_focal_loss=False, use_focal_obj_loss=False, use_softmax_loss=False, use_giou_loss=False, use_diou_loss=False):
    'Return yolo4_loss tensor\n\n    Parameters\n    ----------\n    yolo_outputs: list of tensor, the output of yolo_body or tiny_yolo_body\n    y_true: list of array, the output of preprocess_true_boxes\n    anchors: array, shape=(N, 2), wh\n    num_classes: integer\n    ignore_thresh: float, the iou threshold whether to ignore object confidence loss\n\n    Returns\n    -------\n    loss: tensor, shape=(1,)\n\n    '
    num_layers = (len(anchors) // 3)
    yolo_outputs = args[:num_layers]
    y_true = args[num_layers:]
    anchor_mask = ([[6, 7, 8], [3, 4, 5], [0, 1, 2]] if (num_layers == 3) else [[3, 4, 5], [0, 1, 2]])
    input_shape = K.cast((K.shape(yolo_outputs[0])[1:3] * 32), K.dtype(y_true[0]))
    grid_shapes = [K.cast(K.shape(yolo_outputs[l])[1:3], K.dtype(y_true[0])) for l in range(num_layers)]
    loss = 0
    total_location_loss = 0
    total_confidence_loss = 0
    total_class_loss = 0
    m = K.shape(yolo_outputs[0])[0]
    mf = K.cast(m, K.dtype(yolo_outputs[0]))
    for l in range(num_layers):
        object_mask = y_true[l][(..., 4:5)]
        true_class_probs = y_true[l][(..., 5:)]
        if label_smoothing:
            true_class_probs = _smooth_labels(true_class_probs, label_smoothing)
        (grid, raw_pred, pred_xy, pred_wh) = yolo_head(yolo_outputs[l], anchors[anchor_mask[l]], num_classes, input_shape, calc_loss=True)
        pred_box = K.concatenate([pred_xy, pred_wh])
        raw_true_xy = ((y_true[l][(..., :2)] * grid_shapes[l][::(- 1)]) - grid)
        raw_true_wh = K.log(((y_true[l][(..., 2:4)] / anchors[anchor_mask[l]]) * input_shape[::(- 1)]))
        raw_true_wh = K.switch(object_mask, raw_true_wh, K.zeros_like(raw_true_wh))
        box_loss_scale = (2 - (y_true[l][(..., 2:3)] * y_true[l][(..., 3:4)]))
        ignore_mask = tf.TensorArray(K.dtype(y_true[0]), size=1, dynamic_size=True)
        object_mask_bool = K.cast(object_mask, 'bool')

        def loop_body(b, ignore_mask):
            true_box = tf.boolean_mask(y_true[l][(b, ..., 0:4)], object_mask_bool[(b, ..., 0)])
            iou = box_iou(pred_box[b], true_box)
            best_iou = K.max(iou, axis=(- 1))
            ignore_mask = ignore_mask.write(b, K.cast((best_iou < ignore_thresh), K.dtype(true_box)))
            return ((b + 1), ignore_mask)
        (_, ignore_mask) = tf.while_loop((lambda b, *args: (b < m)), loop_body, [0, ignore_mask])
        ignore_mask = ignore_mask.stack()
        ignore_mask = K.expand_dims(ignore_mask, (- 1))
        if use_focal_obj_loss:
            confidence_loss = sigmoid_focal_loss(object_mask, raw_pred[(..., 4:5)])
        else:
            confidence_loss = ((object_mask * K.binary_crossentropy(object_mask, raw_pred[(..., 4:5)], from_logits=True)) + (((1 - object_mask) * K.binary_crossentropy(object_mask, raw_pred[(..., 4:5)], from_logits=True)) * ignore_mask))
        if use_focal_loss:
            if use_softmax_loss:
                class_loss = softmax_focal_loss(true_class_probs, raw_pred[(..., 5:)])
            else:
                class_loss = sigmoid_focal_loss(true_class_probs, raw_pred[(..., 5:)])
        elif use_softmax_loss:
            class_loss = (object_mask * K.expand_dims(K.categorical_crossentropy(true_class_probs, raw_pred[(..., 5:)], from_logits=True), axis=(- 1)))
        else:
            class_loss = (object_mask * K.binary_crossentropy(true_class_probs, raw_pred[(..., 5:)], from_logits=True))
        if use_giou_loss:
            raw_true_box = y_true[l][(..., 0:4)]
            giou = box_giou(pred_box, raw_true_box)
            giou_loss = ((object_mask * box_loss_scale) * (1 - giou))
            giou_loss = (K.sum(giou_loss) / mf)
            location_loss = giou_loss
        elif use_diou_loss:
            raw_true_box = y_true[l][(..., 0:4)]
            diou = box_diou(pred_box, raw_true_box)
            diou_loss = ((object_mask * box_loss_scale) * (1 - diou))
            diou_loss = (K.sum(diou_loss) / mf)
            location_loss = diou_loss
        else:
            xy_loss = ((object_mask * box_loss_scale) * K.binary_crossentropy(raw_true_xy, raw_pred[(..., 0:2)], from_logits=True))
            wh_loss = (((object_mask * box_loss_scale) * 0.5) * K.square((raw_true_wh - raw_pred[(..., 2:4)])))
            xy_loss = (K.sum(xy_loss) / mf)
            wh_loss = (K.sum(wh_loss) / mf)
            location_loss = (xy_loss + wh_loss)
        confidence_loss = (K.sum(confidence_loss) / mf)
        class_loss = (K.sum(class_loss) / mf)
        loss += ((location_loss + confidence_loss) + class_loss)
        total_location_loss += location_loss
        total_confidence_loss += confidence_loss
        total_class_loss += class_loss
    loss = K.expand_dims(loss, axis=(- 1))
    return loss
