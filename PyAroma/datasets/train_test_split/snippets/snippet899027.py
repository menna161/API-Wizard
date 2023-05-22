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


@parameterized.parameters('random', 'diazo')
def test_make_train_test_split(self, splitting_type):
    'An integration test on a small dataset.'
    fpath = self.temp_dir
    main_train_val_test_fractions = train_test_split_utils.TrainValTestFractions(0.5, 0.25, 0.25)
    replicates_val_test_fractions = train_test_split_utils.TrainValTestFractions(0.0, 0.5, 0.5)
    (mainlib_inchikey_dict, replicates_inchikey_dict, component_inchikey_dict) = make_train_test_split.make_mainlib_replicates_train_test_split(self.mol_list_large, self.mol_list_small, splitting_type, main_train_val_test_fractions, replicates_val_test_fractions)
    make_train_test_split.write_mainlib_split_datasets(component_inchikey_dict, mainlib_inchikey_dict, fpath, ms_constants.MAX_ATOMS, ms_constants.MAX_PEAK_LOC)
    make_train_test_split.write_replicates_split_datasets(component_inchikey_dict, replicates_inchikey_dict, fpath, ms_constants.MAX_ATOMS, ms_constants.MAX_PEAK_LOC)
    for experiment_setup in ds_constants.EXPERIMENT_SETUPS_LIST:
        tf.logging.info('Writing experiment setup for %s', experiment_setup.json_name)
        make_train_test_split.check_experiment_setup(experiment_setup.experiment_setup_dataset_dict, component_inchikey_dict)
        make_train_test_split.write_json_for_experiment(experiment_setup, fpath)
        dict_from_json = json.load(tf.gfile.Open(os.path.join(fpath, experiment_setup.json_name)))
        tf.logging.info(dict_from_json)
        library_files = (dict_from_json[ds_constants.LIBRARY_MATCHING_OBSERVED_KEY] + dict_from_json[ds_constants.LIBRARY_MATCHING_PREDICTED_KEY])
        library_files = [os.path.join(fpath, fname) for fname in library_files]
        hparams = tf.contrib.training.HParams(max_atoms=ms_constants.MAX_ATOMS, max_mass_spec_peak_loc=ms_constants.MAX_PEAK_LOC, intensity_power=1.0, batch_size=5)
        parse_sdf_utils.validate_spectra_array_contents(os.path.join(fpath, dict_from_json[ds_constants.SPECTRUM_PREDICTION_TRAIN_KEY][0]), hparams, os.path.join(fpath, dict_from_json[ds_constants.TRAINING_SPECTRA_ARRAY_KEY]))
        dataset = parse_sdf_utils.get_dataset_from_record(library_files, hparams, mode=tf.estimator.ModeKeys.EVAL, all_data_in_one_batch=True)
        feature_names = [fmap_constants.INCHIKEY]
        label_names = [fmap_constants.ATOM_WEIGHTS]
        (features, labels) = parse_sdf_utils.make_features_and_labels(dataset, feature_names, label_names, mode=tf.estimator.ModeKeys.EVAL)
        with tf.Session() as sess:
            (feature_values, _) = sess.run([features, labels])
        inchikeys_from_file = [ikey[0] for ikey in feature_values[fmap_constants.INCHIKEY].tolist()]
        length_from_info_file = sum([parse_sdf_utils.parse_info_file(library_fname)['num_examples'] for library_fname in library_files])
        self.assertLen(inchikeys_from_file, length_from_info_file)
        inchikey_list_large = [self.encode(ikey) for ikey in self.inchikey_list_large]
        self.assertSetEqual(set(inchikeys_from_file), set(inchikey_list_large))
