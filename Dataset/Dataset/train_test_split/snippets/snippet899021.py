from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import json
import os
import tempfile
from absl.testing import absltest
from absl.testing import parameterized
import dataset_setup_constants as ds_constants
import feature_map_constants as fmap_constants
import make_train_test_split
import mass_spec_constants as ms_constants
import parse_sdf_utils
import test_utils
import train_test_split_utils
import six
import tensorflow as tf


def test_all_lists_mutually_exclusive(self):
    list1 = ['1', '2', '3']
    list2 = ['2', '3', '4']
    try:
        train_test_split_utils.assert_all_lists_mutally_exclusive([list1, list2])
        raise ValueError('Sets with overlapping elements should have failed.')
    except ValueError:
        pass
