import tensorflow as tf
from dps.utils import Parameterized, Param
from dps.utils.tf import tf_shape, tf_binomial_coefficient, build_scheduled_value
from auto_yolo.models.core import concrete_binary_sample_kl, tf_safe_log, logistic_log_pdf


def __call__(self, tensors, existing_objects=None):
    obj_pre_sigmoid = tensors['obj_pre_sigmoid']
    obj_log_odds = tensors['obj_log_odds']
    obj_prob = tensors['obj_prob']
    obj = tensors['obj']
    (batch_size, n_objects, _) = tf_shape(obj)
    max_n_objects = n_objects
    if (existing_objects is not None):
        (_, n_existing_objects, _) = tf_shape(existing_objects)
        existing_objects = tf.reshape(existing_objects, (batch_size, n_existing_objects))
        max_n_objects += n_existing_objects
    count_support = tf.range((max_n_objects + 1), dtype=tf.float32)
    if (self.count_prior_dist is not None):
        assert (len(self.count_prior_dist) == (max_n_objects + 1))
        count_distribution = tf.constant(self.count_prior_dist, dtype=tf.float32)
    else:
        count_prior_prob = tf.nn.sigmoid(self.count_prior_log_odds)
        count_distribution = (count_prior_prob ** count_support)
    normalizer = tf.reduce_sum(count_distribution)
    count_distribution = (count_distribution / tf.maximum(normalizer, 1e-06))
    count_distribution = tf.tile(count_distribution[(None, :)], (batch_size, 1))
    if (existing_objects is not None):
        count_so_far = tf.reduce_sum(tf.round(existing_objects), axis=1, keepdims=True)
        count_distribution = ((count_distribution * tf_binomial_coefficient(count_support, count_so_far)) * tf_binomial_coefficient((max_n_objects - count_support), (n_existing_objects - count_so_far)))
        normalizer = tf.reduce_sum(count_distribution, axis=1, keepdims=True)
        count_distribution = (count_distribution / tf.maximum(normalizer, 1e-06))
    else:
        count_so_far = tf.zeros((batch_size, 1), dtype=tf.float32)
    obj_kl = []
    for i in range(n_objects):
        p_z_given_Cz_raw = ((count_support[(None, :)] - count_so_far) / (max_n_objects - i))
        p_z_given_Cz = tf.clip_by_value(p_z_given_Cz_raw, 0.0, 1.0)
        inv_p_z_given_Cz_raw = ((((max_n_objects - i) - count_support[(None, :)]) + count_so_far) / (max_n_objects - i))
        inv_p_z_given_Cz = tf.clip_by_value(inv_p_z_given_Cz_raw, 0.0, 1.0)
        p_z = tf.reduce_sum((count_distribution * p_z_given_Cz), axis=1, keepdims=True)
        if self.use_concrete_kl:
            prior_log_odds = (tf_safe_log(p_z) - tf_safe_log((1 - p_z)))
            _obj_kl = concrete_binary_sample_kl(obj_pre_sigmoid[(:, i, :)], obj_log_odds[(:, i, :)], self.obj_concrete_temp, prior_log_odds, self.obj_concrete_temp)
        else:
            prob = obj_prob[(:, i, :)]
            _obj_kl = ((prob * (tf_safe_log(prob) - tf_safe_log(p_z))) + ((1 - prob) * (tf_safe_log((1 - prob)) - tf_safe_log((1 - p_z)))))
        obj_kl.append(_obj_kl)
        sample = tf.to_float((obj[(:, i, :)] > 0.5))
        mult = ((sample * p_z_given_Cz) + ((1 - sample) * inv_p_z_given_Cz))
        raw_count_distribution = (mult * count_distribution)
        normalizer = tf.reduce_sum(raw_count_distribution, axis=1, keepdims=True)
        normalizer = tf.maximum(normalizer, 1e-06)
        count_distribution = (raw_count_distribution / normalizer)
        count_so_far += sample
        count_so_far = tf.round(count_so_far)
    obj_kl = tf.reshape(tf.concat(obj_kl, axis=1), (batch_size, n_objects, 1))
    return obj_kl
