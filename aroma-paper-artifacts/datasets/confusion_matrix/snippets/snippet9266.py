from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
import constants as const
import nets.batch_augment as batch_augment
import utils.os_utils as os_utils
import os
from nets import resnet_utils


def __init__(self, cfg=None, is_training=True, global_pool=True, output_stride=None, spatial_squeeze=True, reuse=None, scope='resnet_v2_50', images_ph=None, lbls_ph=None):
    self.cfg = cfg
    batch_size = None
    if (lbls_ph is not None):
        self.gt_lbls = tf.reshape(lbls_ph, [(- 1), cfg.num_classes])
    else:
        self.gt_lbls = tf.placeholder(tf.int32, shape=(batch_size, cfg.num_classes), name='class_lbls')
    self.do_augmentation = tf.placeholder(tf.bool, name='do_augmentation')
    self.loss_class_weight = tf.placeholder(tf.float32, shape=(cfg.num_classes, cfg.num_classes), name='weights')
    if ('honda' in cfg.db_name):
        self.input = tf.placeholder(tf.float32, shape=(batch_size, const.frame_height, const.frame_width, const.context_channels), name='context_input')
    else:
        self.input = tf.placeholder(tf.float32, shape=(batch_size, const.max_frame_size, const.max_frame_size, const.frame_channels), name='context_input')
    if (images_ph is not None):
        self.input = images_ph
        (_, w, h, c) = self.input.shape
        aug_imgs = tf.reshape(self.input, [(- 1), w, h, 3])
        print('No nnutils Augmentation')
    elif ('honda' in cfg.db_name):
        aug_imgs = self.input
    else:
        aug_imgs = tf.cond(self.do_augmentation, (lambda : batch_augment.augment(self.input, cfg.preprocess_func, horizontal_flip=True, vertical_flip=False, rotate=0, crop_probability=0, color_aug_probability=0)), (lambda : batch_augment.center_crop(self.input, cfg.preprocess_func)))
    with slim.arg_scope(resnet_arg_scope()):
        (_, train_end_points) = resnet_v2_50(aug_imgs, cfg.num_classes, is_training=True, global_pool=global_pool, output_stride=output_stride, spatial_squeeze=spatial_squeeze, reuse=reuse, scope=scope)
        (_, val_end_points) = resnet_v2_50(aug_imgs, cfg.num_classes, is_training=False, global_pool=global_pool, output_stride=output_stride, spatial_squeeze=spatial_squeeze, reuse=True, scope=scope)

    def cal_metrics(end_points):
        gt = tf.argmax(self.gt_lbls, 1)
        logits = tf.reshape(end_points['resnet_v2_50/logits'], [(- 1), cfg.num_classes])
        pre_logits = end_points['resnet_v2_50/block4/unit_3/bottleneck_v2']
        center_supervised_cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.gt_lbls, logits=logits, name='xentropy_center')
        loss = tf.reduce_mean(center_supervised_cross_entropy, name='xentropy_mean')
        predictions = tf.reshape(end_points['predictions'], [(- 1), cfg.num_classes])
        class_prediction = tf.argmax(predictions, 1)
        supervised_correct_prediction = tf.equal(gt, class_prediction)
        supervised_correct_prediction_cast = tf.cast(supervised_correct_prediction, tf.float32)
        accuracy = tf.reduce_mean(supervised_correct_prediction_cast)
        confusion_mat = tf.confusion_matrix(gt, class_prediction, num_classes=cfg.num_classes)
        (_, accumulated_accuracy) = tf.metrics.accuracy(gt, class_prediction)
        (_, per_class_acc_acc) = tf.metrics.mean_per_class_accuracy(gt, class_prediction, num_classes=cfg.num_classes)
        per_class_acc_acc = tf.reduce_mean(per_class_acc_acc)
        return (loss, pre_logits, accuracy, confusion_mat, accumulated_accuracy, per_class_acc_acc, class_prediction)
    (self.train_loss, self.train_pre_logits, self.train_accuracy, self.train_confusion_mat, self.train_accumulated_accuracy, self.train_per_class_acc_acc, self.train_class_prediction) = cal_metrics(train_end_points)
    (self.val_loss, self.val_pre_logits, self.val_accuracy, self.val_confusion_mat, self.val_accumulated_accuracy, self.val_per_class_acc_acc, self.val_class_prediction) = cal_metrics(val_end_points)
