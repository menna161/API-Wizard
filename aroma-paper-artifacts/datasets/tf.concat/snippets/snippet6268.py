import tensorflow as tf


def call(self, dec_input, dec_hidden, enc_output):
    (context_vector, attention_weights) = self.attention(dec_hidden, enc_output)
    x = self.embedding(dec_input)
    x = tf.concat([tf.expand_dims(context_vector, 1), x], axis=(- 1))
    (output, state) = self.gru(x)
    output = tf.reshape(output, ((- 1), output.shape[2]))
    x = self.fc(output)
    return (x, state, attention_weights)
