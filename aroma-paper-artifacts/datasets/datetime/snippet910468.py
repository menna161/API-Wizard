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
    d = self.d[(:, ['FSC-A', 'FSC-H', 'FSC-W', 'SSC-A', 'SSC-H', 'SSC-W', 'FSC PMT-A', 'FSC PMT-H', 'FSC PMT-W', 'GFP-A', 'GFP-H', 'mCherry-A', 'mCherry-H'])]
    self.assertEqual(d.acquisition_time, 4)
