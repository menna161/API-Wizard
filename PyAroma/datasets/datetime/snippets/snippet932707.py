from __future__ import division
import math
import os
import datetime
import pprint
import scipy.misc
import numpy as np
import pretty_midi as pm
import copy
import config
import write_midi
import tensorflow as tf
from imageio import imread as _imread


def save_midis(bars, file_path, tempo=80.0):
    padded_bars = np.concatenate((np.zeros((bars.shape[0], bars.shape[1], 24, bars.shape[3])), bars, np.zeros((bars.shape[0], bars.shape[1], 20, bars.shape[3]))), axis=2)
    pause = np.zeros((bars.shape[0], 64, 128, bars.shape[3]))
    images_with_pause = padded_bars
    images_with_pause = images_with_pause.reshape((- 1), 64, padded_bars.shape[2], padded_bars.shape[3])
    images_with_pause_list = []
    for ch_idx in range(padded_bars.shape[3]):
        images_with_pause_list.append(images_with_pause[(:, :, :, ch_idx)].reshape(images_with_pause.shape[0], images_with_pause.shape[1], images_with_pause.shape[2]))
    write_midi.write_piano_rolls_to_midi(images_with_pause_list, program_nums=[0], is_drum=[False], filename=file_path, tempo=tempo, beat_resolution=4)
