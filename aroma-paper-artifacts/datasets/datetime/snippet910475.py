import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_slicing_channel_with_string_array(self):
    '\n        Testing the channel slicing with a string array of a FCSData\n        object.\n\n        '
    ds = self.d[(:, ['FSC-H', 'FL3-H'])]
    self.assertIsInstance(ds, FlowCal.io.FCSData)
    self.assertEqual(ds.shape, (self.n_samples, 2))
    self.assertEqual(ds.channels, ('FSC-H', 'FL3-H'))
