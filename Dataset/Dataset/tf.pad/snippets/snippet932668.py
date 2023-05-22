from __future__ import division
import tensorflow as tf
from ops import *
from utils import *


def generator_resnet(image, options, reuse=False, name='generator'):
    with tf.variable_scope(name):
        if reuse:
            tf.get_variable_scope().reuse_variables()
        else:
            assert (tf.get_variable_scope().reuse is False)

        def residule_block(x, dim, ks=3, s=1, name='res'):
            p = int(((ks - 1) / 2))
            y = tf.pad(x, [[0, 0], [p, p], [p, p], [0, 0]], 'REFLECT')
            y = instance_norm(conv2d(y, dim, ks, s, padding='VALID', name=(name + '_c1')), (name + '_bn1'))
            y = tf.pad(tf.nn.relu(y), [[0, 0], [p, p], [p, p], [0, 0]], 'REFLECT')
            y = instance_norm(conv2d(y, dim, ks, s, padding='VALID', name=(name + '_c2')), (name + '_bn2'))
            return relu((y + x))
        c0 = tf.pad(image, [[0, 0], [3, 3], [3, 3], [0, 0]], 'REFLECT')
        c1 = relu(instance_norm(conv2d(c0, options.gf_dim, 7, 1, padding='VALID', name='g_e1_c'), 'g_e1_bn'))
        c2 = relu(instance_norm(conv2d(c1, (options.gf_dim * 2), 3, 2, name='g_e2_c'), 'g_e2_bn'))
        c3 = relu(instance_norm(conv2d(c2, (options.gf_dim * 4), 3, 2, name='g_e3_c'), 'g_e3_bn'))
        r1 = residule_block(c3, (options.gf_dim * 4), name='g_r1')
        r2 = residule_block(r1, (options.gf_dim * 4), name='g_r2')
        r3 = residule_block(r2, (options.gf_dim * 4), name='g_r3')
        r4 = residule_block(r3, (options.gf_dim * 4), name='g_r4')
        r5 = residule_block(r4, (options.gf_dim * 4), name='g_r5')
        r6 = residule_block(r5, (options.gf_dim * 4), name='g_r6')
        r7 = residule_block(r6, (options.gf_dim * 4), name='g_r7')
        r8 = residule_block(r7, (options.gf_dim * 4), name='g_r8')
        r9 = residule_block(r8, (options.gf_dim * 4), name='g_r9')
        r10 = residule_block(r9, (options.gf_dim * 4), name='g_r10')
        d1 = relu(instance_norm(deconv2d(r10, (options.gf_dim * 2), 3, 2, name='g_d1_dc'), 'g_d1_bn'))
        d2 = relu(instance_norm(deconv2d(d1, options.gf_dim, 3, 2, name='g_d2_dc'), 'g_d2_bn'))
        d3 = tf.pad(d2, [[0, 0], [3, 3], [3, 3], [0, 0]], 'REFLECT')
        pred = tf.nn.sigmoid(conv2d(d3, options.output_c_dim, 7, 1, padding='VALID', name='g_pred_c'))
        return pred
