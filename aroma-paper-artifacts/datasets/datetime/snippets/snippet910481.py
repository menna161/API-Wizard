import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_2d_slicing_assignment(self):
    '\n        Test assignment to FCSData using slicing.\n\n        '
    ds = self.d.copy()
    ds[(:, [1, 2])] = 5
    self.assertIsInstance(ds, FlowCal.io.FCSData)
    self.assertEqual(ds.channels, ('FSC-H', 'SSC-H', 'FL1-H', 'FL2-H', 'FL3-H', 'Time'))
    np.testing.assert_array_equal(ds[(:, 0)], self.d[(:, 0)])
    np.testing.assert_array_equal(ds[(:, 1)], 5)
    np.testing.assert_array_equal(ds[(:, 2)], 5)
    np.testing.assert_array_equal(ds[(:, 3)], self.d[(:, 3)])
    np.testing.assert_array_equal(ds[(:, 4)], self.d[(:, 4)])
