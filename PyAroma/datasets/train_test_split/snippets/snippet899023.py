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


def test_make_mol_list_from_inchikey_dict(self):
    mol_list = train_test_split_utils.make_mol_list_from_inchikey_dict(self.inchikey_dict_large, self.inchikey_list_large)
    self.assertCountEqual(mol_list, self.mol_list_large)
