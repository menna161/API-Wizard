import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_attribute_many(self):
    '\n        Testing correct reporting of hist_bins for many channels.\n        '
    self.assert_list_of_arrays_equal(self.d[0].hist_bins(['SSC-H', 'FL2-H', 'FL3-H'], scale='linear'), [(np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5)])
    self.assert_list_of_arrays_equal(self.d[1].hist_bins(['FITC-A', 'PE-A', 'PE-Cy7-A'], scale='linear'), [(np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(1025) - 0.5)])
    self.assert_list_of_arrays_equal(self.d[2].hist_bins(['FSC', 'SSC', 'TIME'], scale='linear'), [(np.arange(1025) - 0.5), (np.arange(1025) - 0.5), (np.arange(262145) - 0.5)])
    self.assert_list_of_arrays_equal(self.d[3].hist_bins(['FSC PMT-A', 'FSC PMT-H', 'FSC PMT-W'], scale='linear'), [(np.arange(262145) - 0.5), (np.arange(262145) - 0.5), (np.arange(262145) - 0.5)])
