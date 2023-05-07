import numpy as np
import tensorflow as tf
from official.utils.accelerator import tpu as tpu_utils


def construct_embedding_and_values(self, embedding_dim, vocab_size, sequence_length, batch_size, seed):
    np.random.seed(seed)
    embeddings = np.random.random(size=(vocab_size, embedding_dim))
    embedding_table = tf.convert_to_tensor(embeddings, dtype=tf.float32)
    tokens = np.random.randint(low=1, high=(vocab_size - 1), size=(batch_size, sequence_length))
    for i in range(batch_size):
        tokens[(i, np.random.randint(low=0, high=(sequence_length - 1)):)] = 0
    values = tf.convert_to_tensor(tokens, dtype=tf.int32)
    mask = tf.to_float(tf.not_equal(values, 0))
    return (embedding_table, values, mask)
