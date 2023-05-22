import tensorflow as tf
from utils.tf_functions import clip_by_value


def point_form(boxes):
    '\n    将boxes的坐标从(cx,cy, w, h)转换为(xmin, ymin, xmax, ymax)格式\n    :param boxes:\n    :return:\n    '
    return tf.concat(values=[(boxes[(:, :2)] - (boxes[(:, 2:)] / 2)), (boxes[(:, :2)] + (boxes[(:, 2:)] / 2))], axis=1)
