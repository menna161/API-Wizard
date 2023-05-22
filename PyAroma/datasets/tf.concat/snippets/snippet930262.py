from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
from preprocessing import autoaugment


def _ten_crop(image, crop_h, crop_w):

    def _crop(img, center_offset):
        img = tf.image.extract_glimpse([img], [crop_w, crop_h], offsets=tf.to_float([center_offset]), centered=False, normalized=False)
        return tf.squeeze(img, 0)

    def _crop5(img):
        im_shape = tf.shape(image)
        (height, width) = (im_shape[0], im_shape[1])
        (ch, cw) = (tf.to_int32((height / 2)), tf.to_int32((width / 2)))
        (hh, hw) = (tf.to_int32((crop_h / 2)), tf.to_int32((crop_w / 2)))
        ct = _crop(img, [ch, cw])
        lu = _crop(img, [hh, hw])
        ld = _crop(img, [(height - hh), hw])
        ru = _crop(img, [hh, (width - hw)])
        rd = _crop(img, [(height - hh), (width - hw)])
        org_images = tf.stack([lu, ru, ld, rd, ct])
        return (org_images, tf.stack([lu, ru, ld, rd, ct]))
    (lhs, aa_lhs) = _crop5(image)
    rhs = tf.image.flip_left_right(lhs)
    return tf.concat([lhs, rhs], axis=0)
