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
    '\n        Testing correct reporting of resolution after slicing.\n\n        '
    self.assertListEqual(self.d[0][(:, ['SSC-H', 'FL2-H', 'FL3-H'])].resolution(), [1024, 1024, 1024])
    self.assertListEqual(self.d[1][(:, ['FITC-A', 'PE-A', 'PE-Cy7-A'])].resolution(), [1024, 1024, 1024])
    self.assertListEqual(self.d[2][(:, ['FSC', 'SSC', 'TIME'])].resolution(), [1024, 1024, 262144])
    self.assertListEqual(self.d[3][(:, ['FSC PMT-A', 'FSC PMT-H', 'FSC PMT-W'])].resolution(), [262144, 262144, 262144])
