from datetime import datetime, timedelta
from warnings import warn
import numpy as np
from astropy.utils.decorators import classproperty
from astropy.utils.exceptions import ErfaWarning
from .ufunc import get_leap_seconds, set_leap_seconds, dt_eraLEAPSECOND


@classproperty
def expires(cls):
    'The expiration date of the current ERFA table.\n\n        This is either a date inferred from the last table used to update or\n        set the leap-second array, or a number of days beyond the last leap\n        second.\n        '
    if (cls._expires is None):
        last = cls.get()[(- 1)]
        return (datetime(last['year'], last['month'], 1) + timedelta(cls._expiration_days))
    else:
        return cls._expires
