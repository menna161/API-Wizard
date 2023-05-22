from rdkit import Chem
import numpy as np
import tensorflow as tf
import parse_sdf_utils
import train_test_split_utils
import feature_utils
import mass_spec_constants as ms_constants
import similarity as similarity_lib


def make_spectra_array(mol_list):
    'Grab spectra pertaining to same molecule in one np.array.\n    Args:\n      mol_list: list of rdkit.Mol objects. Each Mol should contain \n          information about the spectra, as stored in NIST.\n    Output: \n      np.array of spectra of shape (number of spectra, max spectra length)\n    '
    mass_spec_spectra = np.zeros((len(mol_list), ms_constants.MAX_PEAK_LOC))
    for (idx, mol) in enumerate(mol_list):
        spectra_str = mol.GetProp(ms_constants.SDF_TAG_MASS_SPEC_PEAKS)
        (spectral_locs, spectral_intensities) = feature_utils.parse_peaks(spectra_str)
        dense_mass_spec = feature_utils.make_dense_mass_spectra(spectral_locs, spectral_intensities, ms_constants.MAX_PEAK_LOC)
        mass_spec_spectra[(idx, :)] = dense_mass_spec
    return mass_spec_spectra
