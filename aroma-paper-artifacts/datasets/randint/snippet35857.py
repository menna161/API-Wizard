from typing import List, Tuple
import tensorflow as tf
import random


def data_batch(self, batch_size, shuffle=False):
    '\n        Reads data, normalizes it, shuffles it, then batches it, returns a\n        the next element in dataset op and the dataset initializer op.\n        Inputs:\n            batch_size: Number of images/masks in each batch returned.\n            augment: Boolean, whether to augment data or not.\n            shuffle: Boolean, whether to shuffle data in buffer or not.\n            one_hot_encode: Boolean, whether to one hot encode the mask image or not.\n                            Encoding will done according to the palette specified when\n                            initializing the object.\n        Returns:\n            data: A tf dataset object.\n        '
    data = tf.data.Dataset.from_tensor_slices((self.image_paths, self.mask_paths))
    data = data.map(self._map_function, num_parallel_calls=AUTOTUNE)
    if shuffle:
        data = data.prefetch(AUTOTUNE).shuffle(random.randint(0, len(self.image_paths))).batch(batch_size)
    else:
        data = data.batch(batch_size).prefetch(AUTOTUNE)
    return data
