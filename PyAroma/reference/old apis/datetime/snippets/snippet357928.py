import datetime
from astral import hours_to_time
from astral.sidereal import gmst, lmst


def test_gmst_with_time():
    dt = datetime.datetime(1987, 4, 10, 19, 21, 0)
    mean_sidereal_time = gmst(dt)
    t = hours_to_time((mean_sidereal_time / 15))
    assert (t.hour == 8)
    assert (t.minute == 34)
    assert (t.second == 57)
    assert (t.microsecond == 89578)
