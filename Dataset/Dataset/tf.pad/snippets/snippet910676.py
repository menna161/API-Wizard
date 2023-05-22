import gin.tf
import tensorflow.compat.v1 as tf


def __call__(self, example_string):
    'Processes a single example string.\n\n    Extracts and processes the image, and ignores the label. We assume that the\n    image has three channels.\n\n    Args:\n      example_string: str, an Example protocol buffer.\n\n    Returns:\n      image_rescaled: the image, resized to `image_size x image_size` and\n      rescaled to [-1, 1]. Note that Gaussian data augmentation may cause values\n      to go beyond this range.\n    '
    image_string = tf.parse_single_example(example_string, features={'image': tf.FixedLenFeature([], dtype=tf.string), 'label': tf.FixedLenFeature([], tf.int64)})['image']
    image_decoded = tf.image.decode_image(image_string, channels=3)
    image_decoded.set_shape([None, None, 3])
    image_resized = tf.image.resize_images(image_decoded, [self.image_size, self.image_size], method=tf.image.ResizeMethod.BILINEAR, align_corners=True)
    image = tf.cast(image_resized, tf.float32)
    if (self.data_augmentation is not None):
        if self.data_augmentation.enable_random_brightness:
            delta = self.data_augmentation.random_brightness_delta
            image = tf.image.random_brightness(image, delta)
        if self.data_augmentation.enable_random_saturation:
            delta = self.data_augmentation.random_saturation_delta
            image = tf.image.random_saturation(image, (1 - delta), (1 + delta))
        if self.data_augmentation.enable_random_contrast:
            delta = self.data_augmentation.random_contrast_delta
            image = tf.image.random_contrast(image, (1 - delta), (1 + delta))
        if self.data_augmentation.enable_random_hue:
            delta = self.data_augmentation.random_hue_delta
            image = tf.image.random_hue(image, delta)
        if self.data_augmentation.enable_random_flip:
            image = tf.image.random_flip_left_right(image)
    image = (2 * ((image / 255.0) - 0.5))
    if (self.data_augmentation is not None):
        if self.data_augmentation.enable_gaussian_noise:
            image = (image + (tf.random_normal(tf.shape(image)) * self.data_augmentation.gaussian_noise_std))
        if self.data_augmentation.enable_jitter:
            j = self.data_augmentation.jitter_amount
            paddings = tf.constant([[j, j], [j, j], [0, 0]])
            image = tf.pad(image, paddings, 'REFLECT')
            image = tf.image.random_crop(image, [self.image_size, self.image_size, 3])
    return image
