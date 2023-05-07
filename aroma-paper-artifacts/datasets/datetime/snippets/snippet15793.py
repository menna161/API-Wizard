from datetime import datetime
from sap.cf_logging.defaults import UNIX_EPOCH
from sap.cf_logging.record import util


def test_iso_time_format():
    ' test util.iso_time_format builds ISO date string '
    date = datetime(2017, 1, 5, 1, 2, 3, 2000)
    assert (util.iso_time_format(date) == '2017-01-05T01:02:03.002Z')
