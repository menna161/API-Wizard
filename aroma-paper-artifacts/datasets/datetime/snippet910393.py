import datetime
import os
import six
import unittest
import warnings
import numpy as np
import FlowCal.io
import cPickle as pickle
import pickle


def test_parse_fcs2(self):
    '\n        Test that _parse_time_string() interprets the FCS2.0 time format.\n\n        '
    t = FlowCal.io.FCSData._parse_time_string('20:15:43')
    self.assertEqual(t, datetime.time(20, 15, 43))
