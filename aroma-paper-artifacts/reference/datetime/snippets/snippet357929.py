import datetime
from astral import hours_to_time
from astral.sidereal import gmst, lmst


def test_local_mean_sidereal_time():
    dt = datetime.datetime(1987, 4, 10, 0, 0, 0)
    mean_sidereal_time = lmst(dt, (- 0.13))
    assert (mean_sidereal_time == (197.693195090862 - 0.13))
