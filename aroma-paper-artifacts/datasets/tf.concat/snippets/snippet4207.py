import tensorflow as tf


def call(self, inputs, **kwargs):
    with tf.name_scope('deep_multiply'):
        inputs = tf.concat(inputs, (- 1))
        for (i, hs) in enumerate(self.hiddens):
            with tf.name_scope('deep'):
                deep1 = DeepBlock(hidden=hs, activation=self.activation, prefix='deep_multiply1_{}'.format(i), sparse=self.sparse)(inputs)
                deep2 = DeepBlock(hidden=hs, activation=self.activation, prefix='deep_multiply2_{}'.format(i), sparse=self.sparse)(inputs)
                inputs = ((deep1 + deep2) + tf.multiply(deep1, deep2))
        return inputs
