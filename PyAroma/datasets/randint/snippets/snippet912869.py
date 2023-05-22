from .custom_driver import client, use_browser
from .slot import find_slot
from .utils import log
from .util_game import close_modal
import time
from random import randint
from .village import open_building, open_village, open_city, open_building_type, building
from datetime import timedelta


def upgrade_units_smithy_thread(browser: client, village: int, units: list, interval: int) -> None:
    time.sleep(randint(0, 10))
    while True:
        sleep_time: int = interval
        rv = upgrade_units_smithy(browser, village, units)
        if (rv != (- 1)):
            if (rv is None):
                log('smithy is busy.')
            else:
                sleep_time = rv
                log((('smithy is busy. going to sleep for ' + '{:0>8}'.format(str(timedelta(seconds=sleep_time)))) + '.'))
        time.sleep(sleep_time)
