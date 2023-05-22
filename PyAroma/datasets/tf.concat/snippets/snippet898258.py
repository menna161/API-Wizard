import tensorflow as tf
from net.ops import random_bbox, bbox2mask, local_patch
from net.ops import gan_wgan_loss, gradients_penalty, random_interpolates
from net.ops import free_form_mask_tf
from util.util import f2uint
from functools import partial


def build_generator(self, x, mask, reuse=False, name='inpaint_net'):
    xshape = x.get_shape().as_list()
    (xh, xw) = (xshape[1], xshape[2])
    ones_x = tf.ones_like(x)[(:, :, :, 0:1)]
    xin = x
    x_w_mask = tf.concat([x, ones_x, (ones_x * mask)], axis=3)
    cnum = self.config.g_cnum
    conv_5 = self.conv5
    conv_3 = self.conv3
    with tf.variable_scope(name, reuse=reuse):
        x = conv_5(inputs=x_w_mask, filters=cnum, strides=1, name='conv1')
        x = conv_3(inputs=x, filters=(2 * cnum), strides=2, name='conv2_downsample')
        x = conv_3(inputs=x, filters=(2 * cnum), strides=1, name='conv3')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=2, name='conv4_downsample')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, name='conv5')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, name='conv6')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, dilation_rate=2, name='conv7_atrous')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, dilation_rate=4, name='conv8_atrous')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, dilation_rate=8, name='conv9_atrous')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, dilation_rate=16, name='conv10_atrous')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, name='conv11')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, name='conv12')
        x = tf.image.resize_nearest_neighbor(x, [(xh // 2), (xw // 2)], align_corners=True)
        with tf.variable_scope('conv13_upsample'):
            x = conv_3(inputs=x, filters=(2 * cnum), strides=1, name='conv13_upsample_conv')
        x = conv_3(inputs=x, filters=(2 * cnum), strides=1, name='conv14')
        x = tf.image.resize_nearest_neighbor(x, [xh, xw], align_corners=True)
        with tf.variable_scope('conv15_upsample'):
            x = conv_3(inputs=x, filters=cnum, strides=1, name='conv15_upsample_conv')
        x = conv_3(inputs=x, filters=(cnum // 2), strides=1, name='conv16')
        x = tf.layers.conv2d(inputs=x, kernel_size=3, filters=3, strides=1, activation=None, padding='SAME', name='conv18')
        x_coarse = tf.clip_by_value(x, (- 1.0), 1.0)
        x = ((x_coarse * mask) + (xin * (1 - mask)))
        x_w_mask = tf.concat([x, ones_x, (ones_x * mask)], axis=3)
        x = conv_5(inputs=x_w_mask, filters=cnum, strides=1, name='xconv1')
        x = conv_3(inputs=x, filters=(2 * cnum), strides=2, name='xconv2_downsample')
        x = conv_3(inputs=x, filters=(2 * cnum), strides=1, name='xconv3')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=2, name='xconv4_downsample')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, name='xconv5')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, name='xconv6')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, dilation_rate=2, name='xconv7_atrous')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, dilation_rate=4, name='xconv8_atrous')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, dilation_rate=8, name='xconv9_atrous')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, dilation_rate=16, name='xconv10_atrous')
        x_hallu = x
        x = conv_5(inputs=x_w_mask, filters=cnum, strides=1, name='sconv1')
        x = conv_3(inputs=x, filters=(2 * cnum), strides=2, name='sconv2_downsample')
        x = conv_3(inputs=x, filters=(2 * cnum), strides=1, name='sconv3')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=2, name='sconv4_downsample')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, name='sconv5')
        x = tf.layers.conv2d(x, filters=(4 * cnum), kernel_size=3, strides=1, padding='SAME', name='sconv6', activation=None)
        (x, layout, loss_orth) = att_normalization(x, name='sn')
        x = tf.nn.elu(x)
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, name='sconv7')
        sn_ret = conv_3(inputs=x, filters=(4 * cnum), strides=1, name='sconv8')
        x = tf.concat([x_hallu, sn_ret], axis=3)
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, name='fconv11')
        x = conv_3(inputs=x, filters=(4 * cnum), strides=1, name='fconv12')
        x = tf.image.resize_nearest_neighbor(x, [(xh // 2), (xw // 2)], align_corners=True)
        with tf.variable_scope('fconv13_upsample'):
            x = conv_3(inputs=x, filters=(2 * cnum), strides=1, name='fconv13_upsample_conv')
        x = conv_3(inputs=x, filters=(2 * cnum), strides=1, name='fconv14')
        x = tf.image.resize_nearest_neighbor(x, [xh, xw], align_corners=True)
        with tf.variable_scope('fconv15_upsample'):
            x = conv_3(inputs=x, filters=cnum, strides=1, name='fconv15_upsample_conv')
        x = conv_3(inputs=x, filters=(cnum // 2), strides=1, name='fconv16')
        x = tf.layers.conv2d(inputs=x, kernel_size=3, filters=3, strides=1, activation=None, padding='SAME', name='fconv18')
        x = tf.clip_by_value(x, (- 1.0), 1.0)
    return (x_coarse, x, layout, loss_orth)
