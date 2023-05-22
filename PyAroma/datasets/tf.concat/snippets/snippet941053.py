import tensorflow as tf
from configuration import VARIANCE, NMS_THRESHOLD, CONFIDENCE_THRESHOLD, MAX_BOXES_NUM
from core.anchor import DefaultBoxes


@staticmethod
def _decode(loc, priors, variances):
    boxes = tf.concat(values=[(priors[(:, :2)] + ((loc[(:, :2)] * variances[0]) * priors[(:, 2:)])), (priors[(:, 2:)] * tf.math.exp((loc[(:, 2:)] * variances[1])))], axis=1)
    min_xy = (boxes[(:, :2)] - (boxes[(:, 2:)] / 2))
    max_xy = (boxes[(:, :2)] + (boxes[(:, 2:)] / 2))
    return tf.concat(values=[min_xy, max_xy], axis=1)
