import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_acquisition_time_btim_etim(self):
    '\n        Testing acquisition time using the btim/etim method.\n\n        '
    d = self.d[(:, ['FSC-H', 'SSC-H', 'FL1-H', 'FL2-H', 'FL3-H'])]
    self.assertEqual(d.acquisition_time, 77)
