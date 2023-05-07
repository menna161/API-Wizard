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
    '\n        Testing correct reporting of amp. type after slicing.\n\n        '
    self.assertEqual(self.d[0][(:, 'FSC-H')].amplification_type(), [(0, 0)])
    self.assertEqual(self.d[1][(:, 'FITC-A')].amplification_type(), [(4, 1)])
    self.assertEqual(self.d[2][(:, 'SSC')].amplification_type(), [(0, 0)])
    self.assertEqual(self.d[3][(:, 'GFP-A')].amplification_type(), [(0, 0)])
