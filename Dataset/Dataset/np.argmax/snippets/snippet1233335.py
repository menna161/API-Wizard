import os
import subprocess
import StringIO
import scipy.io.wavfile as wav
import numpy as np
import processor
from nabu.processing.feature_computers import feature_computer_factory


def __call__(self, dataline):
    'process the data in dataline\n\t\tArgs:\n\t\t\tdataline: either a path to a wav file or a command to read and pipe\n\t\t\t\tan audio file\n\n\t\tReturns:\n\t\t\tsegmented_data: The segmented targets as a list of numpy arrays per segment length\n\t\t\tutt_info: some info on the utterance'
    utt_info = dict()
    splitdatalines = dataline.strip().split(' ')
    clean_features = None
    for splitdataline in splitdatalines:
        (rate, utt) = _read_wav(splitdataline)
        features = self.comp(utt, rate)
        features = np.expand_dims(features, 2)
        if (clean_features is None):
            clean_features = features
        else:
            clean_features = np.append(clean_features, features, 2)
    winner = np.argmax(clean_features, axis=2)
    targets = np.empty([features.shape[0], self.dim], dtype=bool)
    for (s_ind, spk_id) in enumerate(self.nrS_select):
        targets[(:, s_ind::len(self.nrS_select))] = (winner == spk_id)
    segmented_data = self.segment_data(targets)
    return (segmented_data, utt_info)
