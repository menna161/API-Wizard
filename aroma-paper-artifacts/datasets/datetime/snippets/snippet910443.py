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
    '\n        Testing correct reporting of channel_labels after slicing.\n\n        '
    self.assertListEqual(self.d[0][(:, 'FSC-H')].channel_labels(), [None])
    self.assertListEqual(self.d[1][(:, 'FITC-A')].channel_labels(), [None])
    self.assertListEqual(self.d[2][(:, 'SSC')].channel_labels(), [None])
    self.assertListEqual(self.d[3][(:, 'GFP-A')].channel_labels(), [None])
    self.assertListEqual(self.d[4][(:, 'Bi209Di')].channel_labels(), ['209Bi_CD11b'])
