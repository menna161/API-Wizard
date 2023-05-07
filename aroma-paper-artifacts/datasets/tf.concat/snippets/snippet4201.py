import tensorflow as tf


def call(self, raw_inputs, **kwargs):
    outputs = []
    with tf.name_scope('deep'):
        output = tf.concat(raw_inputs, (- 1))
        for (i, hs) in enumerate(self.hidden):
            output = CustomDropout(0.1)(output)
            output = DeepBlock(hidden=hs, activation=self.activation, prefix='deep_{}'.format(i), sparse=self.sparse)(output)
            outputs.append(output)
        '\n            H: column wise matrix of each deep layer\n            '
        H = tf.stack(outputs, axis=2)
        "\n            S = H' * H\n            "
        S = tf.matmul(tf.transpose(H, perm=[0, 2, 1]), H)
        '\n            Column wise softmax as attention\n            '
        attention = tf.nn.softmax(S, axis=1)
        '\n            G = H * A\n            '
        G = tf.matmul(H, attention)
        '\n            Sum over deep layers\n            '
        G = tf.reduce_sum(G, axis=(- 1))
        if self.concat_last_deep:
            return tf.concat([outputs[(- 1)], G], axis=(- 1))
        else:
            return G
