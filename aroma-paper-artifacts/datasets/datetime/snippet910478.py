import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_mask_slicing(self):
    '\n        Testing mask slicing of a FCSData object.\n\n        '
    m = (self.d[(:, 1)] > 500)
    ds = self.d[(m, :)]
    self.assertIsInstance(ds, FlowCal.io.FCSData)
    self.assertEqual(ds.channels, ('FSC-H', 'SSC-H', 'FL1-H', 'FL2-H', 'FL3-H', 'Time'))
