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
    '\n        Testing correct reporting of detector voltage after slicing.\n\n        '
    self.assertEqual(self.d[0][(:, ['SSC-H', 'FL2-H', 'FL3-H'])].detector_voltage(), [460, 900, 999])
    self.assertEqual(self.d[1][(:, ['FITC-A', 'PE-A', 'PE-Cy7-A'])].detector_voltage(), [478, 470, 854])
    self.assertEqual(self.d[2][(:, ['FSC', 'SSC', 'FL1'])].detector_voltage(), [10, 460, 501])
    self.assertEqual(self.d[3][(:, ['FSC PMT-A', 'FSC PMT-H', 'FSC PMT-W'])].detector_voltage(), [550, 550, 550])
