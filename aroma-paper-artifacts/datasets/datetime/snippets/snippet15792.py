from datetime import datetime
from sap.cf_logging.defaults import UNIX_EPOCH
from sap.cf_logging.record import util


def test_epoch_nano_second():
    ' test util.epoch_nano_second calculates correctly '
    date = datetime(2017, 1, 1, 0, 0, 0, 12)
    nanoseconds = 1483228800000012000
    assert (util.epoch_nano_second(date) == nanoseconds)
