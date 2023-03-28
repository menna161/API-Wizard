import datetime
from almost_equal import datetime_almost_equal


def test_not_equal(self):
    d1 = datetime.datetime(2019, 1, 1)
    d2 = datetime.datetime(2019, 1, 1, 12, 2, 0)
    assert (not datetime_almost_equal(d1, d2))
