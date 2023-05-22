import reconstructor
from nabu.postprocessing import data_reader
from nabu.processing.feature_computers import base
from abc import ABCMeta, abstractmethod
import os
import numpy as np


def reconstruct_signals_opt_frame_perm(self, output, target):
    'reconstruct the signals, using optimal frame-level permutations\n\n\t\tArgs:\n\t\t\toutput: the output of a single utterance of the neural network\n\t\t\ttarget: the target of a single utterance of the neural network\n\n\t\tReturns:\n\t\t\tthe reconstructed signals\n\t\t\tsome info on the utterance'
    (mixture, utt_info) = self.org_mix_reader(self.pos)
    masks = self._get_masks_opt_frame_perm(output, target, utt_info)
    for (ind, start_index) in enumerate(self.org_mix_reader.start_index_set):
        if (start_index > self.pos):
            processor = self.org_mix_reader.processors[(ind - 1)]
            comp_conf = processor.comp.conf
            break
    reconstructed_signals = list()
    for spk in range(self.nrS):
        spec_est = (mixture * masks[(spk, :, :)])
        if (('scipy' in comp_conf) and (comp_conf['scipy'] == 'True')):
            rec_signal = base.spec2time_scipy(spec_est, utt_info['rate'], utt_info['siglen'], comp_conf)
        else:
            rec_signal = base.spec2time(spec_est, utt_info['rate'], utt_info['siglen'], comp_conf)
        reconstructed_signals.append(rec_signal)
    return (reconstructed_signals, utt_info)
