import utils
import tensorflow as tf
import logging


@staticmethod
def multi_scale_style_swap(content_features, style_features, patch_size=5):
    c_shape = tf.shape(content_features)
    s_shape = tf.shape(style_features)
    channel_assertion = tf.Assert(tf.equal(c_shape[3], s_shape[3]), ['number of channels  must be the same'])
    with tf.control_dependencies([channel_assertion]):
        (c_height, c_width, c_channel) = (c_shape[1], c_shape[2], c_shape[3])
        proposed_outputs = []
        for beta in [(1.0 / 2), (1.0 / (2 ** 0.5)), 1.0]:
            new_height = tf.cast(tf.multiply(tf.cast(s_shape[1], tf.float32), beta), tf.int32)
            new_width = tf.cast(tf.multiply(tf.cast(s_shape[2], tf.float32), beta), tf.int32)
            tmp_style_features = tf.image.resize_images(style_features, [new_height, new_width], method=tf.image.ResizeMethod.BILINEAR)
            style_kernels = tf.extract_image_patches(tmp_style_features, ksizes=[1, patch_size, patch_size, 1], strides=[1, 1, 1, 1], rates=[1, 1, 1, 1], padding='SAME')
            style_kernels = tf.squeeze(style_kernels, axis=0)
            style_kernels = tf.transpose(style_kernels, perm=[2, 0, 1])
            deconv_kernels = tf.reshape(style_kernels, shape=(patch_size, patch_size, c_channel, (- 1)))
            kernels_norm = tf.norm(style_kernels, axis=0, keep_dims=True)
            kernels_norm = tf.reshape(kernels_norm, shape=(1, 1, 1, (- 1)))
            mask = tf.ones((c_height, c_width), tf.float32)
            fullmask = tf.zeros((((c_height + patch_size) - 1), ((c_width + patch_size) - 1)), tf.float32)
            for x in range(patch_size):
                for y in range(patch_size):
                    paddings = [[x, ((patch_size - x) - 1)], [y, ((patch_size - y) - 1)]]
                    padded_mask = tf.pad(mask, paddings=paddings, mode='CONSTANT')
                    fullmask += padded_mask
            pad_width = int(((patch_size - 1) / 2))
            deconv_norm = tf.slice(fullmask, [pad_width, pad_width], [c_height, c_width])
            deconv_norm = tf.reshape(deconv_norm, shape=(1, c_height, c_width, 1))
            pad_total = (patch_size - 1)
            pad_beg = (pad_total // 2)
            pad_end = (pad_total - pad_beg)
            paddings = [[0, 0], [pad_beg, pad_end], [pad_beg, pad_end], [0, 0]]
            net = tf.pad(content_features, paddings=paddings, mode='REFLECT')
            net = tf.nn.conv2d(net, tf.div(deconv_kernels, (kernels_norm + 1e-07)), strides=[1, 1, 1, 1], padding='VALID')
            best_match_ids = tf.argmax(net, axis=3)
            best_match_ids = tf.cast(tf.one_hot(best_match_ids, depth=tf.shape(net)[3]), dtype=tf.float32)
            unnormalized_output = tf.nn.conv2d_transpose(value=best_match_ids, filter=deconv_kernels, output_shape=(c_shape[0], (c_height + pad_total), (c_width + pad_total), c_channel), strides=[1, 1, 1, 1], padding='VALID')
            unnormalized_output = tf.slice(unnormalized_output, [0, pad_beg, pad_beg, 0], c_shape)
            output = tf.div(unnormalized_output, deconv_norm)
            output = tf.reshape(output, shape=c_shape)
            proposed_outputs.append(output)
        proposed_outputs.append(content_features)
        return proposed_outputs
