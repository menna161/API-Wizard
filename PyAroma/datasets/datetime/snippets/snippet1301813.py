from datetime import datetime, timedelta
from warnings import warn
import numpy as np
from astropy.utils.decorators import classproperty
from astropy.utils.exceptions import ErfaWarning
from .ufunc import get_leap_seconds, set_leap_seconds, dt_eraLEAPSECOND


@classmethod
def validate(cls, table):
    "Validate a leap-second table.\n\n        Parameters\n        ----------\n        table : array_like\n            Must have 'year', 'month', and 'tai_utc' entries.  If a 'day'\n            entry is present, it will be checked that it is always 1.\n            If ``table`` has an 'expires' attribute, it will be interpreted\n            as an expiration date.\n\n        Returns\n        -------\n        array : `~numpy.ndarray`\n            Structures array with 'year', 'month', 'tai_utc'.\n        expires: `~datetime.datetime` or None\n            Possible expiration date inferred from the table.  `None` if not\n            present or if not a `~datetime.datetime` or `~astropy.time.Time`\n            instance and not parsable as a 'dd month yyyy' string.\n\n        Raises\n        ------\n        ValueError\n            If the leap seconds in the table are not on the 1st of January or\n            July, or if the sorted TAI-UTC do not increase in increments of 1.\n        "
    try:
        day = table['day']
    except Exception:
        day = 1
    expires = getattr(table, 'expires', None)
    if ((expires is not None) and (not isinstance(expires, datetime))):
        isot = getattr(expires, 'isot', None)
        try:
            if (isot is not None):
                expires = datetime.strptime(isot.partition('T')[0], '%Y-%m-%d')
            else:
                expires = datetime.strptime(expires, '%d %B %Y')
        except Exception as exc:
            warn(f'ignoring non-datetime expiration {expires}; parsing it raised {exc!r}', ErfaWarning)
            expires = None
    if hasattr(table, '__array__'):
        table = table.__array__()[list(dt_eraLEAPSECOND.names)]
    table = np.array(table, dtype=dt_eraLEAPSECOND, copy=False, ndmin=1)
    if (table.ndim > 1):
        raise ValueError('can only pass in one-dimensional tables.')
    if (not np.all(((((day == 1) & (table['month'] == 1)) | (table['month'] == 7)) | (table['year'] < 1972)))):
        raise ValueError('leap seconds inferred that are not on 1st of January or 1st of July.')
    if np.any(((table['year'][:(- 1)] > 1970) & (np.diff(table['tai_utc']) != 1))):
        raise ValueError('jump in TAI-UTC by something else than one.')
    return (table, expires)
