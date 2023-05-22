import os
import warnings
import numpy as np
from astropy.utils.exceptions import AstropyUserWarning, AstropyDeprecationWarning
import h5py
from astropy.table import Table, meta, serialize
from astropy.table import serialize
from astropy.table.table import has_info_class
from astropy import units as u
from astropy.utils.data_info import MixinInfo, serialize_context_as
from astropy.table import meta
from astropy.io import registry as io_registry
from astropy.table import Table
import h5py
import h5py
import yaml
import h5py


def _find_all_structured_arrays(handle):
    '\n    Find all structured arrays in an HDF5 file\n    '
    import h5py
    structured_arrays = []

    def append_structured_arrays(name, obj):
        if (isinstance(obj, h5py.Dataset) and (obj.dtype.kind == 'V')):
            structured_arrays.append(name)
    handle.visititems(append_structured_arrays)
    return structured_arrays
