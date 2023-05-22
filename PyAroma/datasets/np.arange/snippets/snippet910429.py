import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_attribute_single(self):
    '\n        Testing correct reporting of hist_bins for a single channel.\n        '
    np.testing.assert_array_equal(self.d[0].hist_bins('FSC-H', scale='linear'), (np.arange(1025) - 0.5))
    np.testing.assert_array_equal(self.d[1].hist_bins('FITC-A', scale='linear'), (np.arange(1025) - 0.5))
    np.testing.assert_array_equal(self.d[2].hist_bins('SSC', scale='linear'), (np.arange(1025) - 0.5))
    np.testing.assert_array_equal(self.d[3].hist_bins('GFP-A', scale='linear'), (np.arange(262145) - 0.5))
