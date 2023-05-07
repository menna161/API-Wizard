import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_nondefault_nbins_many_1(self):
    '\n        Testing correct generation of hist_bins with a non-default nbins\n        '
    bd = (np.arange(1025) - 0.5)
    xd = np.linspace(0, 1, len(bd))
    xs = np.linspace(0, 1, (256 + 1))
    bins1 = np.interp(xs, xd, bd)
    self.assert_list_of_arrays_equal(self.d[0].hist_bins(['FL1-H', 'FL2-H'], nbins=256, scale='linear'), [bins1, bins1])
