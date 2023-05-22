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


def test_make_train_val_test_split_mol_lists(self):
    main_train_test_split = train_test_split_utils.TrainValTestFractions(0.5, 0.25, 0.25)
    inchikey_list_of_lists = train_test_split_utils.make_train_val_test_split_inchikey_lists(self.inchikey_list_large, self.inchikey_dict_large, main_train_test_split)
    expected_lengths_of_inchikey_lists = [5, 2, 4]
    for (expected_length, inchikey_list) in zip(expected_lengths_of_inchikey_lists, inchikey_list_of_lists):
        self.assertLen(inchikey_list, expected_length)
    train_test_split_utils.assert_all_lists_mutally_exclusive(inchikey_list_of_lists)
    trunc_inchikey_list_large = self.inchikey_list_large[:6]
    inchikey_list_of_lists = [train_test_split_utils.make_train_val_test_split_inchikey_lists(trunc_inchikey_list_large, self.inchikey_dict_large, main_train_test_split)]
    expected_lengths_of_inchikey_lists = [3, 1, 2]
    for (expected_length, inchikey_list) in zip(expected_lengths_of_inchikey_lists, inchikey_list_of_lists):
        self.assertLen(inchikey_list, expected_length)
    train_test_split_utils.assert_all_lists_mutally_exclusive(inchikey_list_of_lists)
