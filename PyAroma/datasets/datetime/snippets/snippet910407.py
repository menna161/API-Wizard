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
    '\n        Testing correct reporting of detector voltage after slicing.\n\n        '
    self.assertEqual(self.d[0][(:, 'FSC-H')].detector_voltage(), [1])
    self.assertEqual(self.d[1][(:, 'FITC-A')].detector_voltage(), [478])
    self.assertEqual(self.d[2][(:, 'SSC')].detector_voltage(), [460])
    self.assertEqual(self.d[3][(:, 'GFP-A')].detector_voltage(), [650])
