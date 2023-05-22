import scorer
import numpy as np
import bss_eval
import itertools
import math


def framesig_padded(sig, frame_len, frame_step, winfunc=(lambda x: np.ones((x,)))):
    '\n\tFrame a signal into overlapping frames. Also pad at the start\n\n\tArgs:\n\t\tsig: the audio signal to frame.\n\t\tframe_len: length of each frame measured in samples.\n\t\tframe_step: number of samples after the start of the previous frame that\n\t\t\tthe next frame should begin.\n\t\twinfunc: the analysis window to apply to each frame. By default no\n\t\t\twindow function is applied.\n\n\tReturns:\n\t\tan array of frames. Size is NUMFRAMES by frame_len.\n\t'
    slen = len(sig)
    if (slen <= frame_len):
        numframes = 1
    else:
        numframes = int(math.ceil(((1.0 * slen) / frame_step)))
    padsignal = np.concatenate((np.zeros(((frame_len / 2) - 1)), sig, np.zeros((frame_len / 2))))
    indices = (np.tile(np.arange(0, frame_len), (numframes, 1)) + np.tile(np.arange(0, (numframes * frame_step), frame_step), (frame_len, 1)).T)
    indices = np.array(indices, dtype=np.int32)
    frames = padsignal[indices]
    win = np.tile(winfunc(frame_len), (numframes, 1))
    return (frames * win)
