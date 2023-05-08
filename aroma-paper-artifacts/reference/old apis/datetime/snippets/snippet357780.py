import datetime
from typing import Union
from astral.julian import julianday_2000


def lmst(at: Union[(datetime.datetime, datetime.date)], longitude: Degrees) -> Degrees:
    'Local Mean Sidereal Time for longitude in degrees\n\n    Args:\n        jd2000: Julian day\n        longitude: Longitude in degrees\n    '
    mst = gmst(at)
    mst += longitude
    return mst
