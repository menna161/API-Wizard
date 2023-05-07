from .custom_driver import client, use_browser
from .settings import settings
import time
from .utils import log, check_for_lines
from .village import open_building, open_city, open_village
from .util_game import close_modal
import schedule
from threading import Thread
from random import randint


def start_farming_thread(browser: client, village: int, farmlists: list, interval: int) -> None:
    time.sleep(randint(0, 10))
    while True:
        start_farming(browser, village, farmlists)
        time.sleep((interval + randint(0, 10)))
