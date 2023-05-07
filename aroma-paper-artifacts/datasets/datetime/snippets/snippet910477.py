import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_2d_slicing(self):
    '\n        Testing 2D slicing of a FCSData object.\n\n        '
    ds = self.d[(:1000, ['SSC-H', 'FL3-H'])]
    self.assertIsInstance(ds, FlowCal.io.FCSData)
    self.assertEqual(ds.shape, (1000, 2))
    self.assertEqual(ds.channels, ('SSC-H', 'FL3-H'))
