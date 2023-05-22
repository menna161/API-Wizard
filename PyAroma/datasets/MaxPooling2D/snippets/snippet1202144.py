import os
import random
import datetime
import re
import math
import logging
from collections import OrderedDict
import multiprocessing
import numpy as np
import skimage.transform
import tensorflow as tf
import keras
import keras.backend as K
import keras.layers as KL
import keras.engine as KE
import keras.models as KM
from keras.callbacks import Callback
from mrcnn import utils
from distutils.version import LooseVersion
import imgaug
import h5py
from keras.engine import topology
from keras.utils.data_utils import get_file
from mrcnn.parallel_model import ParallelModel


def build(self, mode, config):
    'Build Mask R-CNN architecture.\n            input_shape: The shape of the input image.\n            mode: Either "training" or "inference". The inputs and\n                outputs of the model differ accordingly.\n        '
    assert (mode in ['training', 'inference'])
    (h, w) = config.IMAGE_SHAPE[:2]
    if (((h / (2 ** 6)) != int((h / (2 ** 6)))) or ((w / (2 ** 6)) != int((w / (2 ** 6))))):
        raise Exception('Image size must be dividable by 2 at least 6 times to avoid fractions when downscaling and upscaling.For example, use 256, 320, 384, 448, 512, ... etc. ')
    chan = config.IMAGE_CHANNEL_COUNT
    input_image = KL.Input(shape=[None, None, chan], name='input_image')
    input_image_meta = KL.Input(shape=[config.IMAGE_META_SIZE], name='input_image_meta')
    if (mode == 'training'):
        input_rpn_match = KL.Input(shape=[None, 1], name='input_rpn_match', dtype=tf.int32)
        input_rpn_bbox = KL.Input(shape=[None, 4], name='input_rpn_bbox', dtype=tf.float32)
        input_gt_class_ids = KL.Input(shape=[None], name='input_gt_class_ids', dtype=tf.int32)
        input_gt_boxes = KL.Input(shape=[None, 4], name='input_gt_boxes', dtype=tf.float32)
        gt_boxes = KL.Lambda((lambda x: norm_boxes_graph(x, K.shape(input_image)[1:3])))(input_gt_boxes)
        if config.USE_MINI_MASK:
            input_gt_masks = KL.Input(shape=[config.MINI_MASK_SHAPE[0], config.MINI_MASK_SHAPE[1], None], name='input_gt_masks', dtype=bool)
        else:
            input_gt_masks = KL.Input(shape=[config.IMAGE_SHAPE[0], config.IMAGE_SHAPE[1], None], name='input_gt_masks', dtype=bool)
    elif (mode == 'inference'):
        input_anchors = KL.Input(shape=[None, 4], name='input_anchors')
    (_, C2, C3, C4, C5) = resnet_graph(input_image, config.BACKBONE, stage5=True, train_bn=config.TRAIN_BN, dilation=config.DILATION)
    P5 = KL.Conv2D(256, (1, 1), name='fpn_c5p5')(C5)
    P4 = KL.Add(name='fpn_p4add')([KL.UpSampling2D(size=(2, 2), name='fpn_p5upsampled')(P5), KL.Conv2D(256, (1, 1), name='fpn_c4p4')(C4)])
    P3 = KL.Add(name='fpn_p3add')([KL.UpSampling2D(size=(2, 2), name='fpn_p4upsampled')(P4), KL.Conv2D(256, (1, 1), name='fpn_c3p3')(C3)])
    P2 = KL.Add(name='fpn_p2add')([KL.UpSampling2D(size=(2, 2), name='fpn_p3upsampled')(P3), KL.Conv2D(256, (1, 1), name='fpn_c2p2')(C2)])
    P2 = KL.Conv2D(256, (3, 3), padding='SAME', name='fpn_p2')(P2)
    P3 = KL.Conv2D(256, (3, 3), padding='SAME', name='fpn_p3')(P3)
    P4 = KL.Conv2D(256, (3, 3), padding='SAME', name='fpn_p4')(P4)
    P5 = KL.Conv2D(256, (3, 3), padding='SAME', name='fpn_p5')(P5)
    P6 = KL.MaxPooling2D(pool_size=(1, 1), strides=2, name='fpn_p6')(P5)
    rpn_feature_maps = [P2, P3, P4, P5, P6]
    mrcnn_feature_maps = [P2, P3, P4, P5]
    if (mode == 'training'):
        anchors = self.get_anchors(config.IMAGE_SHAPE)
        anchors = np.broadcast_to(anchors, ((config.BATCH_SIZE,) + anchors.shape))
        anchors = KL.Lambda((lambda x: tf.Variable(anchors)), name='anchors')(input_image)
    else:
        anchors = input_anchors
    rpn = build_rpn_model(config.RPN_ANCHOR_STRIDE, len(config.RPN_ANCHOR_RATIOS), 256)
    layer_outputs = []
    for p in rpn_feature_maps:
        layer_outputs.append(rpn([p]))
    output_names = ['rpn_class_logits', 'rpn_class', 'rpn_bbox']
    outputs = list(zip(*layer_outputs))
    outputs = [KL.Concatenate(axis=1, name=n)(list(o)) for (o, n) in zip(outputs, output_names)]
    (rpn_class_logits, rpn_class, rpn_bbox) = outputs
    proposal_count = (config.POST_NMS_ROIS_TRAINING if (mode == 'training') else config.POST_NMS_ROIS_INFERENCE)
    rpn_rois = ProposalLayer(proposal_count=proposal_count, nms_threshold=config.RPN_NMS_THRESHOLD, name='ROI', config=config)([rpn_class, rpn_bbox, anchors])
    if (mode == 'training'):
        active_class_ids = KL.Lambda((lambda x: parse_image_meta_graph(x)['active_class_ids']))(input_image_meta)
        if (not config.USE_RPN_ROIS):
            input_rois = KL.Input(shape=[config.POST_NMS_ROIS_TRAINING, 4], name='input_roi', dtype=np.int32)
            target_rois = KL.Lambda((lambda x: norm_boxes_graph(x, K.shape(input_image)[1:3])))(input_rois)
        else:
            target_rois = rpn_rois
        (rois, target_class_ids, target_bbox, target_mask) = DetectionTargetLayer(config, name='proposal_targets')([target_rois, input_gt_class_ids, gt_boxes, input_gt_masks])
        (mrcnn_class_logits, mrcnn_class, mrcnn_bbox) = fpn_classifier_graph(rois, mrcnn_feature_maps, input_image_meta, config.POOL_SIZE, config.NUM_CLASSES, train_bn=config.TRAIN_BN)
        mrcnn_mask = build_fpn_mask_graph(rois, mrcnn_feature_maps, input_image_meta, config.MASK_POOL_SIZE, config.NUM_CLASSES, train_bn=config.TRAIN_BN)
        output_rois = KL.Lambda((lambda x: (x * 1)), name='output_rois')(rois)
        rpn_class_loss = KL.Lambda((lambda x: rpn_class_loss_graph(*x)), name='rpn_class_loss')([input_rpn_match, rpn_class_logits])
        rpn_bbox_loss = KL.Lambda((lambda x: rpn_bbox_loss_graph(config, *x)), name='rpn_bbox_loss')([input_rpn_bbox, input_rpn_match, rpn_bbox])
        class_loss = KL.Lambda((lambda x: mrcnn_class_loss_graph(*x)), name='mrcnn_class_loss')([target_class_ids, mrcnn_class_logits, active_class_ids])
        bbox_loss = KL.Lambda((lambda x: mrcnn_bbox_loss_graph(*x)), name='mrcnn_bbox_loss')([target_bbox, target_class_ids, mrcnn_bbox])
        mask_loss = KL.Lambda((lambda x: mrcnn_mask_loss_graph(*x)), name='mrcnn_mask_loss')([target_mask, target_class_ids, mrcnn_mask])
        inputs = [input_image, input_image_meta, input_rpn_match, input_rpn_bbox, input_gt_class_ids, input_gt_boxes, input_gt_masks]
        if (not config.USE_RPN_ROIS):
            inputs.append(input_rois)
        outputs = [rpn_class_logits, rpn_class, rpn_bbox, mrcnn_class_logits, mrcnn_class, mrcnn_bbox, mrcnn_mask, rpn_rois, output_rois, rpn_class_loss, rpn_bbox_loss, class_loss, bbox_loss, mask_loss]
        model = KM.Model(inputs, outputs, name='mask_rcnn')
    else:
        (mrcnn_class_logits, mrcnn_class, mrcnn_bbox) = fpn_classifier_graph(rpn_rois, mrcnn_feature_maps, input_image_meta, config.POOL_SIZE, config.NUM_CLASSES, train_bn=config.TRAIN_BN)
        detections = DetectionLayer(config, name='mrcnn_detection')([rpn_rois, mrcnn_class, mrcnn_bbox, input_image_meta])
        detection_boxes = KL.Lambda((lambda x: x[(..., :4)]))(detections)
        mrcnn_mask = build_fpn_mask_graph(detection_boxes, mrcnn_feature_maps, input_image_meta, config.MASK_POOL_SIZE, config.NUM_CLASSES, train_bn=config.TRAIN_BN)
        model = KM.Model([input_image, input_image_meta, input_anchors], [detections, mrcnn_class, mrcnn_bbox, mrcnn_mask, rpn_rois, rpn_class, rpn_bbox], name='mask_rcnn')
    if (config.GPU_COUNT > 1):
        from mrcnn.parallel_model import ParallelModel
        model = ParallelModel(model, config.GPU_COUNT)
    return model
