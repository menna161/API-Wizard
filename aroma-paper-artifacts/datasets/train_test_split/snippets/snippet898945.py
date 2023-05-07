from rdkit import Chem
import numpy as np
import tensorflow as tf
import parse_sdf_utils
import train_test_split_utils
import feature_utils
import mass_spec_constants as ms_constants
import similarity as similarity_lib


def main():
    mol_list = parse_sdf_utils.get_sdf_to_mol('/mnt/storage/NIST_zipped/NIST17/replib_mend.sdf')
    inchikey_dict = train_test_split_utils.make_inchikey_dict(mol_list)
    spectra_for_one_mol = make_spectra_array(inchikey_dict['PDACHFOTOFNHBT-UHFFFAOYSA-N'])
    distance_matrix = get_similarities(spectra_for_one_mol)
    print('distance for spectra in PDACHFOTOFNHBT-UHFFFAOYSA-N', distance_matrix)
