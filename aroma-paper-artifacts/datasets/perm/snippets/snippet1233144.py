from abc import ABCMeta, abstractmethod
import os
import scipy.io.wavfile as wav
import numpy as np


def opt_frame_perm(self, batch_outputs, batch_targets, batch_sequence_lengths):
    ' reconstruct the signals, using the optimal speaker permutations on frame level using the targets, and write\n\t\tthe audio files\n\n\t\tArgs:\n\t\t- batch_outputs: A dictionary containing the batch outputs of the network\n\t\t- batch_outputs: A dictionary containing the batch targets for the outputs\n\t\t- batch_sequence_lengths: A dictionary containing the sequence length for each utterance\n\t\t'
    for utt_ind in range(self.batch_size):
        utt_output = dict()
        for output_name in self.requested_output_names:
            utt_output[output_name] = batch_outputs[output_name][utt_ind][(:batch_sequence_lengths[output_name][utt_ind], :)]
        target_keys = [key for key in batch_targets.keys() if ('target' in key)]
        utt_target = {key: batch_targets[key][utt_ind][(:batch_sequence_lengths[output_name][utt_ind], :)] for key in target_keys}
        (reconstructed_signals, utt_info) = self.reconstruct_signals_opt_frame_perm(utt_output, utt_target)
        self.write_audiofile(reconstructed_signals, utt_info)
        if self.store_output:
            for output_name in self.requested_output_names:
                savename = ((output_name + '_') + utt_info['utt_name'])
                np.save(os.path.join(self.output_dir, savename), utt_output[output_name])
        self.pos += 1
