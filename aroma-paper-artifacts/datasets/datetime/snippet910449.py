import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_acquisition_start_time(self):
    '\n        Testing of acquisition start time.\n\n        '
    time_correct = datetime.datetime(2015, 5, 19, 16, 50, 29)
    self.assertEqual(self.d.acquisition_start_time, time_correct)
