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
    '\n        Testing correct reporting of amp. type after slicing.\n\n        '
    self.assertEqual(self.d[0][(:, ['SSC-H', 'FL2-H', 'FL3-H'])].amplification_type(), [(0, 0), (4, 1), (4, 1)])
    self.assertEqual(self.d[1][(:, ['FITC-A', 'PE-A', 'PE-Cy7-A'])].amplification_type(), [(4, 1), (4, 1), (4, 1)])
    self.assertEqual(self.d[2][(:, ['FSC', 'SSC', 'FL1'])].amplification_type(), [(0, 0), (0, 0), (4, 1)])
    self.assertEqual(self.d[3][(:, ['FSC PMT-A', 'FSC PMT-H', 'FSC PMT-W'])].amplification_type(), [(0, 0), (0, 0), (0, 0)])
