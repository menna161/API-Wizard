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
    '\n        Testing correct reporting of resolution after slicing.\n\n        '
    self.assertListEqual(self.d[0][(:, 'FSC-H')].resolution(), [1024])
    self.assertListEqual(self.d[1][(:, 'FITC-A')].resolution(), [1024])
    self.assertListEqual(self.d[2][(:, 'SSC')].resolution(), [1024])
    self.assertListEqual(self.d[3][(:, 'GFP-A')].resolution(), [262144])
