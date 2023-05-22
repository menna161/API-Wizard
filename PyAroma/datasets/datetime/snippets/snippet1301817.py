from datetime import datetime, timedelta
from warnings import warn
import numpy as np
from astropy.utils.decorators import classproperty
from astropy.utils.exceptions import ErfaWarning
from .ufunc import get_leap_seconds, set_leap_seconds, dt_eraLEAPSECOND


@classmethod
def update(cls, table):
    "Add any leap seconds not already present to the ERFA table.\n\n        This method matches leap seconds with those present in the ERFA table,\n        and extends the latter as necessary.\n\n        If the ERFA leap seconds file was corrupted, it will be reset.\n\n        If the table is corrupted, the ERFA file will be unchanged.\n\n        Parameters\n        ----------\n        table : array_like or `~astropy.utils.iers.LeapSeconds`\n            Array or table with TAI-UTC from leap seconds.  Should have\n            'year', 'month', and 'tai_utc' columns.\n\n        Returns\n        -------\n        n_update : int\n            Number of items updated.\n\n        Raises\n        ------\n        ValueError\n            If the leap seconds in the table are not on the 1st of January or\n            July, or if the sorted TAI-UTC do not increase in increments of 1.\n        "
    (table, expires) = cls.validate(table)
    try:
        (erfa_ls, _) = cls.validate(cls.get())
    except Exception:
        cls.set()
        erfa_ls = cls.get()
    ls = np.union1d(erfa_ls, table)
    cls.set(ls)
    try:
        if ((expires is not None) and (expires > cls.expires)):
            cls._expires = expires
    except Exception as exc:
        warn(("table 'expires' attribute ignored as comparing it with a datetime raised an error:\n" + str(exc)), ErfaWarning)
    return (len(ls) - len(erfa_ls))
