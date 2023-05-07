from datetime import datetime
from sap.cf_logging.defaults import UNIX_EPOCH
from sap.cf_logging.record import util


def test_time_delta_ms():
    ' test time_delta_ms calculates delta between date and unix epoch'
    date = datetime(2017, 1, 1, 0, 0, 0, 12000)
    assert (util.time_delta_ms(UNIX_EPOCH, date) == 1483228800012)
