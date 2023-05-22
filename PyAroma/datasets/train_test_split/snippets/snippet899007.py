from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import json
import os
import random
from absl import app
from absl import flags
import dataset_setup_constants as ds_constants
import mass_spec_constants as ms_constants
import parse_sdf_utils
import train_test_split_utils
import six
import tensorflow as tf


def make_mainlib_replicates_train_test_split(mainlib_mol_list, replicates_mol_list, splitting_type, mainlib_fractions, replicates_fractions, mainlib_maximum_num_molecules_to_use=None, replicates_maximum_num_molecules_to_use=None, rseed=42):
    "Makes train/validation/test inchikey lists from two lists of rdkit.Mol.\n\n  Args:\n    mainlib_mol_list : list of molecules from main library\n    replicates_mol_list : list of molecules from replicates library\n    splitting_type : type of splitting to use for validation splits.\n    mainlib_fractions : TrainValTestFractions namedtuple\n        holding desired fractions for train/val/test split of mainlib\n    replicates_fractions : TrainValTestFractions namedtuple\n        holding desired fractions for train/val/test split of replicates.\n        For the replicates set, the train fraction should be set to 0.\n    mainlib_maximum_num_molecules_to_use : Largest number of molecules to use\n       when making datasets from mainlib\n    replicates_maximum_num_molecules_to_use : Largest number of molecules to use\n       when making datasets from replicates\n    rseed : random seed for shuffling\n\n  Returns:\n    main_inchikey_dict : Dict that is keyed by inchikey, containing a list of\n        rdkit.Mol objects corresponding to that inchikey from the mainlib\n    replicates_inchikey_dict : Dict that is keyed by inchikey, containing a list\n        of rdkit.Mol objects corresponding to that inchikey from the replicates\n        library\n    main_replicates_split_inchikey_lists_dict : dict with keys :\n      'mainlib_train', 'mainlib_validation', 'mainlib_test',\n      'replicates_train', 'replicates_validation', 'replicates_test'\n      Values are lists of inchikeys corresponding to each dataset.\n\n  "
    random.seed(rseed)
    main_inchikey_dict = train_test_split_utils.make_inchikey_dict(mainlib_mol_list)
    main_inchikey_list = main_inchikey_dict.keys()
    if six.PY3:
        main_inchikey_list = list(main_inchikey_list)
    if (mainlib_maximum_num_molecules_to_use is not None):
        main_inchikey_list = random.sample(main_inchikey_list, mainlib_maximum_num_molecules_to_use)
    replicates_inchikey_dict = train_test_split_utils.make_inchikey_dict(replicates_mol_list)
    replicates_inchikey_list = replicates_inchikey_dict.keys()
    if six.PY3:
        replicates_inchikey_list = list(replicates_inchikey_list)
    if (replicates_maximum_num_molecules_to_use is not None):
        replicates_inchikey_list = random.sample(replicates_inchikey_list, replicates_maximum_num_molecules_to_use)
    main_train_validation_test_inchikeys = train_test_split_utils.make_train_val_test_split_inchikey_lists(main_inchikey_list, main_inchikey_dict, mainlib_fractions, holdout_inchikey_list=replicates_inchikey_list, splitting_type=splitting_type)
    replicates_validation_test_inchikeys = train_test_split_utils.make_train_val_test_split_inchikey_lists(replicates_inchikey_list, replicates_inchikey_dict, replicates_fractions, splitting_type=splitting_type)
    component_inchikey_dict = {ds_constants.MAINLIB_TRAIN_BASENAME: main_train_validation_test_inchikeys.train, ds_constants.MAINLIB_VALIDATION_BASENAME: main_train_validation_test_inchikeys.validation, ds_constants.MAINLIB_TEST_BASENAME: main_train_validation_test_inchikeys.test, ds_constants.REPLICATES_TRAIN_BASENAME: replicates_validation_test_inchikeys.train, ds_constants.REPLICATES_VALIDATION_BASENAME: replicates_validation_test_inchikeys.validation, ds_constants.REPLICATES_TEST_BASENAME: replicates_validation_test_inchikeys.test}
    train_test_split_utils.assert_all_lists_mutally_exclusive(list(component_inchikey_dict.values()))
    all_inchikeys_in_components = []
    for ikey_list in list(component_inchikey_dict.values()):
        for ikey in ikey_list:
            all_inchikeys_in_components.append(ikey)
    assert (set((main_inchikey_list + replicates_inchikey_list)) == set(all_inchikeys_in_components)), 'The inchikeys in the original inchikey dictionary are not all included in the train/val/test component libraries'
    return (main_inchikey_dict, replicates_inchikey_dict, component_inchikey_dict)
