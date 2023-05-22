from datetime import datetime, timedelta
from warnings import warn
import numpy as np
from astropy.utils.decorators import classproperty
from astropy.utils.exceptions import ErfaWarning
from .ufunc import get_leap_seconds, set_leap_seconds, dt_eraLEAPSECOND


@classproperty
def expired(cls):
    'Whether the leap second table is valid beyond the present.'
    return (cls.expires < datetime.now())
