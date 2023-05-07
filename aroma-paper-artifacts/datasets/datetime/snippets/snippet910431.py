import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_slice_single_str(self):
    '\n        Testing correct reporting of hist_bins after slicing.\n        '
    self.assert_list_of_arrays_equal(self.d[0][(:, 'FSC-H')].hist_bins(scale='linear'), [(np.arange(1025) - 0.5)])
    self.assert_list_of_arrays_equal(self.d[1][(:, 'FITC-A')].hist_bins(scale='linear'), [(np.arange(1025) - 0.5)])
    self.assert_list_of_arrays_equal(self.d[2][(:, 'SSC')].hist_bins(scale='linear'), [(np.arange(1025) - 0.5)])
    self.assert_list_of_arrays_equal(self.d[3][(:, 'GFP-A')].hist_bins(scale='linear'), [(np.arange(262145) - 0.5)])
