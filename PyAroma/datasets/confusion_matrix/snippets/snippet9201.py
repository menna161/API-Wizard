from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
import constants as const
import nets.batch_augment as batch_augment
import utils.os_utils as os_utils
import os


def cal_metrics(end_points):
    gt = tf.argmax(self.gt_lbls, 1)
    logits = tf.reshape(end_points['densenet161/logits'], [(- 1), num_classes])
    pre_logits = end_points['densenet161/dense_block4']
    center_supervised_cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(labels=self.gt_lbls, logits=logits, name='xentropy_center')
    loss = tf.reduce_mean(center_supervised_cross_entropy, name='xentropy_mean')
    predictions = tf.reshape(end_points['predictions'], [(- 1), num_classes])
    class_prediction = tf.argmax(predictions, 1)
    supervised_correct_prediction = tf.equal(gt, class_prediction)
    supervised_correct_prediction_cast = tf.cast(supervised_correct_prediction, tf.float32)
    accuracy = tf.reduce_mean(supervised_correct_prediction_cast)
    confusion_mat = tf.confusion_matrix(gt, class_prediction, num_classes=num_classes)
    (_, accumulated_accuracy) = tf.metrics.accuracy(gt, class_prediction)
    (_, per_class_acc_acc) = tf.metrics.mean_per_class_accuracy(gt, class_prediction, num_classes=num_classes)
    per_class_acc_acc = tf.reduce_mean(per_class_acc_acc)
    return (loss, pre_logits, accuracy, confusion_mat, accumulated_accuracy, per_class_acc_acc)
