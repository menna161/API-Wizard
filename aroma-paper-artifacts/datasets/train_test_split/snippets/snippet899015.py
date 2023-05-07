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


def main(_):
    tf.gfile.MkDir(FLAGS.output_master_dir)
    main_train_val_test_fractions_tuple = tuple([float(elem) for elem in FLAGS.main_train_val_test_fractions])
    main_train_val_test_fractions = train_test_split_utils.TrainValTestFractions(*main_train_val_test_fractions_tuple)
    replicates_train_val_test_fractions_tuple = tuple([float(elem) for elem in FLAGS.replicates_train_val_test_fractions])
    replicates_train_val_test_fractions = train_test_split_utils.TrainValTestFractions(*replicates_train_val_test_fractions_tuple)
    mainlib_mol_list = parse_sdf_utils.get_sdf_to_mol(FLAGS.main_sdf_name, max_atoms=FLAGS.max_atoms)
    replicates_mol_list = parse_sdf_utils.get_sdf_to_mol(FLAGS.replicates_sdf_name, max_atoms=FLAGS.max_atoms)
    (mainlib_inchikey_dict, replicates_inchikey_dict, component_inchikey_dict) = make_mainlib_replicates_train_test_split(mainlib_mol_list, replicates_mol_list, FLAGS.splitting_type, main_train_val_test_fractions, replicates_train_val_test_fractions, mainlib_maximum_num_molecules_to_use=FLAGS.mainlib_maximum_num_molecules_to_use, replicates_maximum_num_molecules_to_use=FLAGS.replicates_maximum_num_molecules_to_use)
    write_mainlib_split_datasets(component_inchikey_dict, mainlib_inchikey_dict, FLAGS.output_master_dir, FLAGS.max_atoms, FLAGS.max_mass_spec_peak_loc)
    write_replicates_split_datasets(component_inchikey_dict, replicates_inchikey_dict, FLAGS.output_master_dir, FLAGS.max_atoms, FLAGS.max_mass_spec_peak_loc)
    for experiment_setup in ds_constants.EXPERIMENT_SETUPS_LIST:
        check_experiment_setup(experiment_setup.experiment_setup_dataset_dict, component_inchikey_dict)
        write_json_for_experiment(experiment_setup, FLAGS.output_master_dir)
