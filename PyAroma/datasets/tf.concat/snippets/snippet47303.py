import tensorflow as tf
import tensorflow_probability as tfp
import numpy as np
import sonnet as snt
import itertools
from dps import cfg
from dps.utils import Param, AttrDict
from dps.utils.tf import build_scheduled_value, FIXED_COLLECTION, ScopedFunction, tf_shape, apply_object_wise
from auto_yolo.tf_ops import render_sprites, resampler_edge
from auto_yolo.models.core import concrete_binary_pre_sigmoid_sample, coords_to_image_space


def _call(self, objects, background, is_training, appearance_only=False, mask_only=False):
    ' If mask_only==True, then we ignore the provided background, using a black blackground instead,\n            and also ignore the computed appearance, using all-white appearances instead.\n\n        '
    if (not self.initialized):
        self.image_depth = tf_shape(background)[(- 1)]
    single = False
    if isinstance(objects, dict):
        single = True
        objects = [objects]
    _object_maps = []
    _scales = []
    _offsets = []
    _appearance = []
    for (i, obj) in enumerate(objects):
        anchor_box = self.anchor_boxes[i]
        object_shape = self.object_shapes[i]
        object_decoder = self.maybe_build_subnet('object_decoder_for_flight_{}'.format(i), builder_name='build_object_decoder')
        appearance_logit = apply_object_wise(object_decoder, obj.attr, output_size=(object_shape + ((self.image_depth + 1),)), is_training=is_training)
        appearance_logit = (appearance_logit * (([self.color_logit_scale] * self.image_depth) + [self.alpha_logit_scale]))
        appearance_logit = (appearance_logit + (([0.0] * self.image_depth) + [self.alpha_logit_bias]))
        appearance = tf.nn.sigmoid(tf.clip_by_value(appearance_logit, (- 10.0), 10.0))
        _appearance.append(appearance)
        if appearance_only:
            continue
        (batch_size, *obj_leading_shape, _, _, _) = tf_shape(appearance)
        n_objects = np.prod(obj_leading_shape)
        appearance = tf.reshape(appearance, (batch_size, n_objects, *object_shape, (self.image_depth + 1)))
        (obj_colors, obj_alpha) = tf.split(appearance, [self.image_depth, 1], axis=(- 1))
        if mask_only:
            obj_colors = tf.ones_like(obj_colors)
        obj_alpha *= tf.reshape(obj.obj, (batch_size, n_objects, 1, 1, 1))
        z = tf.reshape(obj.z, (batch_size, n_objects, 1, 1, 1))
        obj_importance = tf.maximum(((obj_alpha * z) / self.importance_temp), 0.01)
        object_maps = tf.concat([obj_colors, obj_alpha, obj_importance], axis=(- 1))
        (*_, image_height, image_width, _) = tf_shape(background)
        (yt, xt, ys, xs) = coords_to_image_space(obj.yt, obj.xt, obj.ys, obj.xs, (image_height, image_width), anchor_box, top_left=True)
        scales = tf.concat([ys, xs], axis=(- 1))
        scales = tf.reshape(scales, (batch_size, n_objects, 2))
        offsets = tf.concat([yt, xt], axis=(- 1))
        offsets = tf.reshape(offsets, (batch_size, n_objects, 2))
        _object_maps.append(object_maps)
        _scales.append(scales)
        _offsets.append(offsets)
    if single:
        _appearance = _appearance[0]
    if appearance_only:
        return dict(appearance=_appearance)
    if mask_only:
        background = tf.zeros_like(background)
    output = render_sprites.render_sprites(_object_maps, _scales, _offsets, background)
    return dict(appearance=_appearance, output=output)
