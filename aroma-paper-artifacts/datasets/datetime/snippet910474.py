import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_slicing_channel_with_int_array(self):
    '\n        Testing the channel slicing with an int array of a FCSData\n        object.\n        '
    ds = self.d[(:, [1, 3])]
    self.assertIsInstance(ds, FlowCal.io.FCSData)
    self.assertEqual(ds.shape, (self.n_samples, 2))
    self.assertEqual(ds.channels, ('SSC-H', 'FL2-H'))
