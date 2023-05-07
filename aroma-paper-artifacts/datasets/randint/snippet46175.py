import numpy as np
import random
import copy


def train_sample(data_set, batch_size, source_seq_len, target_seq_len, input_size):
    all_keys = list(data_set.keys())
    chosen_keys_idx = np.random.choice(len(all_keys), batch_size)
    total_seq_len = (source_seq_len + target_seq_len)
    encoder_inputs = np.zeros((batch_size, (source_seq_len - 1), input_size), dtype=np.float32)
    decoder_inputs = np.zeros((batch_size, 1, input_size), dtype=np.float32)
    decoder_outputs = np.zeros((batch_size, target_seq_len, input_size), dtype=np.float32)
    for i in range(batch_size):
        the_key = all_keys[chosen_keys_idx[i]]
        (t, d) = data_set[the_key].shape
        idx = np.random.randint(16, (t - total_seq_len))
        data_sel = data_set[the_key][(idx:(idx + total_seq_len), :)]
        encoder_inputs[(i, :, :)] = data_sel[(0:(source_seq_len - 1), :)]
        decoder_inputs[(i, :, :)] = data_sel[((source_seq_len - 1):source_seq_len, :)]
        decoder_outputs[(i, :, :)] = data_sel[(source_seq_len:, :)]
    rs = int(np.random.uniform(low=0, high=4))
    downsample_idx = np.array([(int(i) + rs) for i in [np.floor((j * 4)) for j in range(12)]])
    return (encoder_inputs, decoder_inputs, decoder_outputs, downsample_idx)
