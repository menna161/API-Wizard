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


def validate(source):
    '\n    Prints a WCS validation report for the given FITS file.\n\n    Parameters\n    ----------\n    source : str path, readable file-like object or `astropy.io.fits.HDUList` object\n        The FITS file to validate.\n\n    Returns\n    -------\n    results : WcsValidateResults instance\n        The result is returned as nested lists.  The first level\n        corresponds to the HDUs in the given file.  The next level has\n        an entry for each WCS found in that header.  The special\n        subclass of list will pretty-print the results as a table when\n        printed.\n    '

    class _WcsValidateWcsResult(list):

        def __init__(self, key):
            self._key = key

        def __repr__(self):
            result = ["  WCS key '{}':".format((self._key or ' '))]
            if len(self):
                for entry in self:
                    for (i, line) in enumerate(entry.splitlines()):
                        if (i == 0):
                            initial_indent = '    - '
                        else:
                            initial_indent = '      '
                        result.extend(textwrap.wrap(line, initial_indent=initial_indent, subsequent_indent='      '))
            else:
                result.append('    No issues.')
            return '\n'.join(result)

    class _WcsValidateHduResult(list):

        def __init__(self, hdu_index, hdu_name):
            self._hdu_index = hdu_index
            self._hdu_name = hdu_name
            list.__init__(self)

        def __repr__(self):
            if len(self):
                if self._hdu_name:
                    hdu_name = f' ({self._hdu_name})'
                else:
                    hdu_name = ''
                result = [f'HDU {self._hdu_index}{hdu_name}:']
                for wcs in self:
                    result.append(repr(wcs))
                return '\n'.join(result)
            return ''

    class _WcsValidateResults(list):

        def __repr__(self):
            result = []
            for hdu in self:
                content = repr(hdu)
                if len(content):
                    result.append(content)
            return '\n\n'.join(result)
    global __warningregistry__
    if isinstance(source, fits.HDUList):
        hdulist = source
    else:
        hdulist = fits.open(source)
    results = _WcsValidateResults()
    for (i, hdu) in enumerate(hdulist):
        hdu_results = _WcsValidateHduResult(i, hdu.name)
        results.append(hdu_results)
        with warnings.catch_warnings(record=True) as warning_lines:
            wcses = find_all_wcs(hdu.header, relax=_wcs.WCSHDR_reject, fix=False, _do_set=False)
        for wcs in wcses:
            wcs_results = _WcsValidateWcsResult(wcs.wcs.alt)
            hdu_results.append(wcs_results)
            try:
                del __warningregistry__
            except NameError:
                pass
            with warnings.catch_warnings(record=True) as warning_lines:
                warnings.resetwarnings()
                warnings.simplefilter('always', FITSFixedWarning, append=True)
                try:
                    WCS(hdu.header, key=(wcs.wcs.alt or ' '), relax=_wcs.WCSHDR_reject, fix=True, _do_set=False)
                except WcsError as e:
                    wcs_results.append(str(e))
                wcs_results.extend([str(x.message) for x in warning_lines])
    return results
