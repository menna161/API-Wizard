import numpy as np


def _melfbank(self):
    linear_freq = 1000.0
    mfbsize = (self.mfbsize - 1)
    bFreq = np.linspace(0, (self.sf / 2.0), ((self.fftl // 2) + 1), dtype=np.float32)
    minMel = self._freq2mel(0.0)
    maxMel = self._freq2mel((self.sf / 2.0))
    iFreq = self._mel2freq(np.linspace(minMel, maxMel, (mfbsize + 2), dtype=np.float32))
    linear_dim = np.where((iFreq < linear_freq))[0].size
    iFreq[:(linear_dim + 1)] = np.linspace(iFreq[0], iFreq[linear_dim], (linear_dim + 1))
    diff = np.diff(iFreq)
    so = np.subtract.outer(iFreq, bFreq)
    lower = ((- so[:mfbsize]) / np.expand_dims(diff[:mfbsize], 1))
    upper = (so[2:] / np.expand_dims(diff[1:], 1))
    fb = np.maximum(0, np.minimum(lower, upper))
    enorm = (2.0 / (iFreq[2:(mfbsize + 2)] - iFreq[:mfbsize]))
    fb *= enorm[(:, np.newaxis)]
    fb0 = np.hstack([np.array(((2.0 * (self.fftl // 2)) / self.sf), np.float32), np.zeros((self.fftl // 2), np.float32)])
    fb = np.vstack([fb0, fb])
    return fb
