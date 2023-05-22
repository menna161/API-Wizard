import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_attribute(self):
    '\n        Testing correct reporting of hist_bins.\n        '
    self.assert_list_of_arrays_equal(self.d[0].hist_bins(scale='linear'), [(np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5)])
    self.assert_list_of_arrays_equal(self.d[1].hist_bins(scale='linear'), [(np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5)])
    self.assert_list_of_arrays_equal(self.d[2].hist_bins(scale='linear'), [(np.arange(262145) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5)])
    self.assert_list_of_arrays_equal(self.d[3].hist_bins(scale='linear'), [(np.arange(262145) - 0.5), (np.arange(262145) - 0.5), (np.arange(262145) - 0.5), (np.arange(262145) - 0.5), (np.arange(262145) - 0.5), (np.arange(262145) - 0.5), (np.arange(262145) - 0.5), (np.arange(262145) - 0.5), (np.arange(262145) - 0.5), (np.arange(262145) - 0.5), (np.arange(262145) - 0.5), (np.arange(262145) - 0.5), (np.arange(262145) - 0.5), (np.arange(262145) - 0.5)])
