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


def test_make_train_val_test_split_mol_lists_family(self):
    train_test_split = train_test_split_utils.TrainValTestFractions(0.5, 0.25, 0.25)
    (train_inchikeys, val_inchikeys, test_inchikeys) = train_test_split_utils.make_train_val_test_split_inchikey_lists(self.inchikey_list_large, self.inchikey_dict_large, train_test_split, holdout_inchikey_list=self.inchikey_list_small, splitting_type='diazo')
    self.assertCountEqual(train_inchikeys, ['UFHFLCQGNIYNRP-UHFFFAOYSA-N', 'CCGKOQOJPYTBIH-UHFFFAOYSA-N', 'ASTNYHRQIBTGNO-UHFFFAOYSA-N', 'UFHFLCQGNIYNRP-VVKOMZTBSA-N', 'PVVBOXUQVSZBMK-UHFFFAOYSA-N'])
    self.assertCountEqual((val_inchikeys + test_inchikeys), ['OWKPLCCVKXABQF-UHFFFAOYSA-N', 'COVPJOWITGLAKX-UHFFFAOYSA-N', 'GKVDXUXIAHWQIK-UHFFFAOYSA-N', 'UCIXUAPVXAZYDQ-VMPITWQZSA-N'])
    (replicate_train_inchikeys, _, replicate_test_inchikeys) = train_test_split_utils.make_train_val_test_split_inchikey_lists(self.inchikey_list_small, self.inchikey_dict_small, train_test_split, splitting_type='diazo')
    self.assertEqual(replicate_train_inchikeys[0], 'PNYUDNYAXSEACV-RVDMUPIBSA-N')
    self.assertEqual(replicate_test_inchikeys[0], 'YXHKONLOYHBTNS-UHFFFAOYSA-N')
