import tensorflow as tf
from utils.tf_functions import clip_by_value


def encode(matched, priors, variances):
    g_cxcy = (((matched[(:, :2)] + matched[(:, 2:)]) / 2) - priors[(:, :2)])
    g_cxcy /= (variances[0] * priors[(:, 2:)])
    g_wh = ((matched[(:, 2:)] - matched[(:, :2)]) / priors[(:, 2:)])
    g_wh = (tf.math.log(g_wh) / variances[1])
    return tf.concat(values=[g_cxcy, g_wh], axis=1)
