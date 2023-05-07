import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_none_slicing_2(self):
    '\n        Testing slicing with None on the second dimension of a FCSData\n        object.\n\n        '
    ds = self.d[(:, None)]
    self.assertIsInstance(ds, np.ndarray)
