import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_nondefault_nbins_many_5(self):
    '\n        Testing correct generation of hist_bins with a non-default nbins\n        '
    bd = (np.arange(1025) - 0.5)
    xd = np.linspace(0, 1, len(bd))
    xs = np.linspace(0, 1, (256 + 1))
    bins1 = np.interp(xs, xd, bd)
    xs = np.linspace(0, 1, (512 + 1))
    bins2 = np.interp(xs, xd, bd)
    self.assert_list_of_arrays_equal(self.d[2].hist_bins(['FL1', 'TIME', 'FL3'], nbins=[256, None, 512], scale='linear'), [bins1, (np.arange(262145) - 0.5), bins2])
