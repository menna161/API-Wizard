from astral import AstralError
from datetime import datetime
from pytz import timezone
from pytz import utc
from firestore import DataError


def utc_now(self):
    'Calculates the current UTC date and time.'
    return utc.localize(datetime.utcnow())
