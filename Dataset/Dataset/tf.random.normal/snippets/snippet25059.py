import math
import code
import tensorflow as tf
import matplotlib.pyplot as plt
import os


def transform_batch(images, max_rot_deg, max_shear_deg, max_zoom_diff_pct, max_shift_pct, experimental_tpu_efficiency=True):
    'Transform a batch of square images with the same randomized affine\n  transformation.\n  '

    def clipped_random():
        rand = tf.random.normal([1], dtype=tf.float32)
        rand = (tf.clip_by_value(rand, (- 2.0), 2.0) / 2.0)
        return rand
    batch_size = images.shape[0]
    tf.debugging.assert_equal(images.shape[1], images.shape[2], 'Images should be square')
    DIM = images.shape[1]
    channels = images.shape[3]
    XDIM = (DIM % 2)
    rot = (max_rot_deg * clipped_random())
    shr = (max_shear_deg * clipped_random())
    h_zoom = (1.0 + (clipped_random() * max_zoom_diff_pct))
    w_zoom = (1.0 + (clipped_random() * max_zoom_diff_pct))
    h_shift = (clipped_random() * (DIM * max_shift_pct))
    w_shift = (clipped_random() * (DIM * max_shift_pct))
    m = get_mat(rot, shr, h_zoom, w_zoom, h_shift, w_shift)
    x = tf.repeat(tf.range((DIM // 2), ((- DIM) // 2), (- 1)), DIM)
    y = tf.tile(tf.range(((- DIM) // 2), (DIM // 2)), [DIM])
    z = tf.ones([(DIM * DIM)], tf.int32)
    idx = tf.stack([x, y, z])
    idx2 = tf.matmul(m, tf.cast(idx, tf.float32))
    idx2 = tf.cast(idx2, tf.int32)
    idx2 = tf.clip_by_value(idx2, ((((- DIM) // 2) + XDIM) + 1), (DIM // 2))
    idx3 = tf.stack([((DIM // 2) - idx2[(0,)]), (((DIM // 2) - 1) + idx2[(1,)])])
    idx3 = tf.transpose(idx3)
    batched_idx3 = tf.tile(idx3[tf.newaxis], [batch_size, 1, 1])
    if experimental_tpu_efficiency:
        idx4 = ((idx3[(:, 0)] * DIM) + idx3[(:, 1)])
        images = tf.reshape(images, [batch_size, (DIM * DIM), channels])
        d = tf.gather(images, idx4, axis=1)
        return tf.reshape(d, [batch_size, DIM, DIM, channels])
    else:
        d = tf.gather_nd(images, batched_idx3, batch_dims=1)
        return tf.reshape(d, [batch_size, DIM, DIM, channels])
