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
    '\n        Testing correct reporting of channel_labels after slicing.\n\n        '
    self.assertListEqual(self.d[0][(:, ['SSC-H', 'FL2-H', 'FL3-H'])].channel_labels(), [None, None, None])
    self.assertListEqual(self.d[1][(:, ['FITC-A', 'PE-A', 'PE-Cy7-A'])].channel_labels(), [None, None, None])
    self.assertListEqual(self.d[2][(:, ['FSC', 'SSC', 'TIME'])].channel_labels(), [None, None, None])
    self.assertListEqual(self.d[3][(:, ['FSC PMT-A', 'FSC PMT-H', 'FSC PMT-W'])].channel_labels(), [None, None, None])
    self.assertListEqual(self.d[4][(:, ['Bi209Di', 'Ce140Di', 'Ce142Di'])].channel_labels(), ['209Bi_CD11b', '140Ce', '142Ce'])
