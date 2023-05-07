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


def setUp(self):
    super(MakeTrainTestSplitTest, self).setUp()
    test_data_directory = test_utils.test_dir('testdata/')
    self.temp_dir = tempfile.mkdtemp(dir=absltest.get_default_test_tmpdir())
    test_sdf_file_large = os.path.join(test_data_directory, 'test_14_mend.sdf')
    test_sdf_file_small = os.path.join(test_data_directory, 'test_2_mend.sdf')
    max_atoms = ms_constants.MAX_ATOMS
    self.mol_list_large = parse_sdf_utils.get_sdf_to_mol(test_sdf_file_large, max_atoms=max_atoms)
    self.mol_list_small = parse_sdf_utils.get_sdf_to_mol(test_sdf_file_small, max_atoms=max_atoms)
    self.inchikey_dict_large = train_test_split_utils.make_inchikey_dict(self.mol_list_large)
    self.inchikey_dict_small = train_test_split_utils.make_inchikey_dict(self.mol_list_small)
    self.inchikey_list_large = list(self.inchikey_dict_large.keys())
    self.inchikey_list_small = list(self.inchikey_dict_small.keys())
