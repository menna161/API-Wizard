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


def read_table_hdf5(input, path=None, character_as_bytes=True):
    '\n    Read a Table object from an HDF5 file\n\n    This requires `h5py <http://www.h5py.org/>`_ to be installed. If more than one\n    table is present in the HDF5 file or group, the first table is read in and\n    a warning is displayed.\n\n    Parameters\n    ----------\n    input : str or :class:`h5py:File` or :class:`h5py:Group` or\n        :class:`h5py:Dataset` If a string, the filename to read the table from.\n        If an h5py object, either the file or the group object to read the\n        table from.\n    path : str\n        The path from which to read the table inside the HDF5 file.\n        This should be relative to the input file or group.\n    character_as_bytes: bool\n        If `True` then Table columns are left as bytes.\n        If `False` then Table columns are converted to unicode.\n    '
    try:
        import h5py
    except ImportError:
        raise Exception('h5py is required to read and write HDF5 files')
    input_save = input
    if isinstance(input, (h5py.File, h5py.Group)):
        if (path is not None):
            try:
                input = input[path]
            except (KeyError, ValueError):
                raise OSError(f'Path {path} does not exist')
        if isinstance(input, h5py.Group):
            arrays = _find_all_structured_arrays(input)
            if (len(arrays) == 0):
                raise ValueError('no table found in HDF5 group {}'.format(path))
            elif (len(arrays) > 0):
                path = (arrays[0] if (path is None) else ((path + '/') + arrays[0]))
                if (len(arrays) > 1):
                    warnings.warn('path= was not specified but multiple tables are present, reading in first available table (path={})'.format(path), AstropyUserWarning)
                return read_table_hdf5(input, path=path)
    elif (not isinstance(input, h5py.Dataset)):
        if hasattr(input, 'read'):
            try:
                input = input.name
            except AttributeError:
                raise TypeError('h5py can only open regular files')
        f = h5py.File(input, 'r')
        try:
            return read_table_hdf5(f, path=path, character_as_bytes=character_as_bytes)
        finally:
            f.close()
    from astropy.table import Table, meta, serialize
    table = Table(np.array(input))
    old_version_meta = (META_KEY in input.attrs)
    new_version_meta = ((path is not None) and (meta_path(path) in input_save))
    if (old_version_meta or new_version_meta):
        if new_version_meta:
            header = meta.get_header_from_yaml((h.decode('utf-8') for h in input_save[meta_path(path)]))
        elif old_version_meta:
            header = meta.get_header_from_yaml((h.decode('utf-8') for h in input.attrs[META_KEY]))
        if ('meta' in list(header.keys())):
            table.meta = header['meta']
        header_cols = dict(((x['name'], x) for x in header['datatype']))
        for col in table.columns.values():
            for attr in ('description', 'format', 'unit', 'meta'):
                if (attr in header_cols[col.name]):
                    setattr(col, attr, header_cols[col.name][attr])
        table = serialize._construct_mixins_from_columns(table)
    else:
        table.meta.update(input.attrs)
    if (not character_as_bytes):
        table.convert_bytestring_to_unicode()
    return table
