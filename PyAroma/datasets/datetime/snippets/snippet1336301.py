from datetime import datetime, timedelta
import pytest
from astropy import _erfa as erfa
from astropy.utils import iers
from astropy.utils.exceptions import AstropyWarning
from astropy.time import update_leap_seconds


def setup(self):
    self.built_in = iers.LeapSeconds.from_iers_leap_seconds()
    self.erfa_ls = iers.LeapSeconds.from_erfa()
    now = datetime.now()
    self.good_enough = (now + timedelta(150))
