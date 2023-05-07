import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_parse_fcs3(self):
    '\n        Test that _parse_time_string() interprets the FCS3.0 time format.\n\n        '
    t = FlowCal.io.FCSData._parse_time_string('20:15:43:20')
    self.assertEqual(t, datetime.time(20, 15, 43, 333333))
