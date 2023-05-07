import chainer
import numpy as np
import onnx_script


def _gen_random_sequence(batch_size, sequence_length, num_vocabs):
    lengths = np.random.randint(2, sequence_length, size=batch_size)
    lengths = np.flip(np.sort(lengths), axis=0)
    lengths[0] = sequence_length
    labels = np.random.randint(2, num_vocabs, size=(batch_size, sequence_length))
    return (labels, lengths)
