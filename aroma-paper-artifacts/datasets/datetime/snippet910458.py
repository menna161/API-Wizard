import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_acquisition_end_time(self):
    '\n        Testing of acquisition end time.\n\n        '
    time_correct = datetime.datetime(2015, 7, 27, 20, 0, 16)
    self.assertEqual(self.d.acquisition_end_time, time_correct)
