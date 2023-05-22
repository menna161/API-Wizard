import copy
import uuid
import io
import itertools
import os
import re
import textwrap
import warnings
import builtins
import numpy as np
from astropy import log
from astropy.io import fits
from . import docstrings
from . import _wcs
from astropy.utils.compat import possible_filename
from astropy.utils.exceptions import AstropyWarning, AstropyUserWarning, AstropyDeprecationWarning
from .wcsapi.fitswcs import FITSWCSAPIMixin, SlicedFITSWCS
from copy import deepcopy


def find_all_wcs(header, relax=True, keysel=None, fix=True, translate_units='', _do_set=True):
    "\n    Find all the WCS transformations in the given header.\n\n    Parameters\n    ----------\n    header : str or astropy.io.fits header object.\n\n    relax : bool or int, optional\n        Degree of permissiveness:\n\n        - `True` (default): Admit all recognized informal extensions of the\n          WCS standard.\n\n        - `False`: Recognize only FITS keywords defined by the\n          published WCS standard.\n\n        - `int`: a bit field selecting specific extensions to accept.\n          See :ref:`relaxread` for details.\n\n    keysel : sequence of flags, optional\n        A list of flags used to select the keyword types considered by\n        wcslib.  When ``None``, only the standard image header\n        keywords are considered (and the underlying wcspih() C\n        function is called).  To use binary table image array or pixel\n        list keywords, *keysel* must be set.\n\n        Each element in the list should be one of the following strings:\n\n            - 'image': Image header keywords\n\n            - 'binary': Binary table image array keywords\n\n            - 'pixel': Pixel list keywords\n\n        Keywords such as ``EQUIna`` or ``RFRQna`` that are common to\n        binary table image arrays and pixel lists (including\n        ``WCSNna`` and ``TWCSna``) are selected by both 'binary' and\n        'pixel'.\n\n    fix : bool, optional\n        When `True` (default), call `~astropy.wcs.Wcsprm.fix` on\n        the resulting objects to fix any non-standard uses in the\n        header.  `FITSFixedWarning` warnings will be emitted if any\n        changes were made.\n\n    translate_units : str, optional\n        Specify which potentially unsafe translations of non-standard\n        unit strings to perform.  By default, performs none.  See\n        `WCS.fix` for more information about this parameter.  Only\n        effective when ``fix`` is `True`.\n\n    Returns\n    -------\n    wcses : list of `WCS` objects\n    "
    if isinstance(header, (str, bytes)):
        header_string = header
    elif isinstance(header, fits.Header):
        header_string = header.tostring()
    else:
        raise TypeError('header must be a string or astropy.io.fits.Header object')
    keysel_flags = _parse_keysel(keysel)
    if isinstance(header_string, str):
        header_bytes = header_string.encode('ascii')
    else:
        header_bytes = header_string
    wcsprms = _wcs.find_all_wcs(header_bytes, relax, keysel_flags)
    result = []
    for wcsprm in wcsprms:
        subresult = WCS(fix=False, _do_set=False)
        subresult.wcs = wcsprm
        result.append(subresult)
        if fix:
            subresult.fix(translate_units)
        if _do_set:
            subresult.wcs.set()
    return result
