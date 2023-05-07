import numpy as np
import random
import copy
import os


def srnn_sample(data_set, action, source_seq_len, target_seq_len, input_size):
    batch_size = 8
    total_frames = (source_seq_len + target_seq_len)
    encoder_inputs = np.zeros((batch_size, (source_seq_len - 1), input_size), dtype=np.float32)
    decoder_inputs = np.zeros((batch_size, 1, input_size), dtype=np.float32)
    decoder_outputs = np.zeros((batch_size, target_seq_len, input_size), dtype=np.float32)
    SEED = 1234567890
    rng = np.random.RandomState(SEED)
    for i in range(batch_size):
        data_sel = data_set[(action, 1, 'even')]
        (t, _) = data_sel.shape
        idx = rng.randint(0, (t - total_frames))
        data_sel = data_sel[(idx:(idx + total_frames), :)]
        encoder_inputs[(i, :, :)] = data_sel[(0:(source_seq_len - 1), :)]
        decoder_inputs[(i, :, :)] = data_sel[((source_seq_len - 1):source_seq_len, :)]
        decoder_outputs[(i, :, :)] = data_sel[(source_seq_len:, :)]
    return (encoder_inputs, decoder_inputs, decoder_outputs)
