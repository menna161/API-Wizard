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
    '\n        Testing correct reporting of amplifier gain after slicing.\n\n        '
    self.assertEqual(self.d[0][(:, ['SSC-H', 'FL2-H', 'FL3-H'])].amplifier_gain(), [None, None, None])
    self.assertEqual(self.d[1][(:, ['FITC-A', 'PE-A', 'PE-Cy7-A'])].amplifier_gain(), [None, None, None])
    self.assertEqual(self.d[2][(:, ['FSC', 'SSC', 'FL1'])].amplifier_gain(), [1.0, 1.0, 1.0])
    self.assertEqual(self.d[3][(:, ['FSC PMT-A', 'FSC PMT-H', 'Time'])].amplifier_gain(), [1.0, 1.0, 0.01])
