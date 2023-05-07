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
    '\n        Testing correct reporting of amplifier gain after slicing.\n\n        '
    self.assertEqual(self.d[0][(:, 'FSC-H')].amplifier_gain(), [None])
    self.assertEqual(self.d[1][(:, 'FITC-A')].amplifier_gain(), [None])
    self.assertEqual(self.d[2][(:, 'SSC')].amplifier_gain(), [1.0])
    self.assertEqual(self.d[3][(:, 'GFP-A')].amplifier_gain(), [1.0])
