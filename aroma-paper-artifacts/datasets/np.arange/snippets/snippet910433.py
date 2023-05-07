import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_nondefault_nbins(self):
    '\n        Testing correct generation of hist_bins with a non-default nbins\n        '
    for nbins in [128, 256, 512]:
        bd = (np.arange(1025) - 0.5)
        xd = np.linspace(0, 1, len(bd))
        xs = np.linspace(0, 1, (nbins + 1))
        bins = np.interp(xs, xd, bd)
        np.testing.assert_array_equal(self.d[0].hist_bins('FSC-H', nbins=nbins, scale='linear'), bins)
