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


def write_all_dataset_files(inchikey_dict, inchikey_list, base_name, output_dir, max_atoms, max_mass_spec_peak_loc, make_library_array=False):
    'Helper function for writing all the files associated with a TFRecord.\n\n  Args:\n    inchikey_dict : Full dictionary keyed by inchikey containing lists of\n                    rdkit.Mol objects\n    inchikey_list : List of inchikeys to include in dataset\n    base_name : Base name for the dataset\n    output_dir : Path for saving all TFRecord files\n    max_atoms : Maximum number of atoms to include for a given molecule\n    max_mass_spec_peak_loc : Largest m/z peak to include in a spectra.\n    make_library_array : Flag for whether to make library array\n  Returns:\n    Saves 3 files:\n     basename.tfrecord : a TFRecord file,\n     basename.inchikey.txt : a text file with all the inchikeys in the dataset\n     basename.tfrecord.info: a text file with one line describing\n         the length of the TFRecord file.\n    Also saves if make_library_array is set:\n     basename.npz : see parse_sdf_utils.write_dicts_to_example\n  '
    record_name = (base_name + TFRECORD_FILENAME_END)
    mol_list = train_test_split_utils.make_mol_list_from_inchikey_dict(inchikey_dict, inchikey_list)
    if make_library_array:
        library_array_pathname = (base_name + NP_LIBRARY_ARRAY_END)
        parse_sdf_utils.write_dicts_to_example(mol_list, os.path.join(output_dir, record_name), max_atoms, max_mass_spec_peak_loc, os.path.join(output_dir, library_array_pathname))
    else:
        parse_sdf_utils.write_dicts_to_example(mol_list, os.path.join(output_dir, record_name), max_atoms, max_mass_spec_peak_loc)
    write_list_of_inchikeys(inchikey_list, base_name, output_dir)
    parse_sdf_utils.write_info_file(mol_list, os.path.join(output_dir, record_name))
