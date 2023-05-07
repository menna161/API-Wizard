import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_slice_many_str(self):
    '\n        Testing correct reporting of hist_bins after slicing.\n        '
    self.assert_list_of_arrays_equal(self.d[0][(:, ['SSC-H', 'FL2-H', 'FL3-H'])].hist_bins(scale='linear'), [(np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5)])
    self.assert_list_of_arrays_equal(self.d[1][(:, ['FITC-A', 'PE-A', 'PE-Cy7-A'])].hist_bins(scale='linear'), [(np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5)])
    self.assert_list_of_arrays_equal(self.d[2][(:, ['FSC', 'SSC', 'TIME'])].hist_bins(scale='linear'), [(np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(262145) - 0.5)])
    self.assert_list_of_arrays_equal(self.d[3][(:, ['FSC PMT-A', 'FSC PMT-H', 'FSC PMT-W'])].hist_bins(scale='linear'), [(np.arange(262145) - 0.5), (np.arange(262145) - 0.5), (np.arange(262145) - 0.5)])
