from datetime import datetime, timedelta
import pytest
from astropy import _erfa as erfa
from astropy.utils import iers
from astropy.utils.exceptions import AstropyWarning
from astropy.time import update_leap_seconds


@pytest.mark.remote_data
def test_never_expired_if_connected(self):
    assert (self.erfa_ls.expires > datetime.now())
    assert (self.erfa_ls.expires >= self.good_enough)
