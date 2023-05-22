import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_slicing_channel_with_int(self):
    '\n        Testing the channel slicing with an int of a FCSData object.\n\n        '
    ds = self.d[(:, 2)]
    self.assertIsInstance(ds, FlowCal.io.FCSData)
    self.assertEqual(ds.shape, (self.n_samples,))
    self.assertEqual(ds.channels, ('FL1-H',))