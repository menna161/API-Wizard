from .custom_driver import client, use_browser
from .settings import settings
import time
from .utils import log, check_for_lines
from .village import open_building, open_city, open_village
from .util_game import close_modal
import schedule
from threading import Thread
from random import randint


def sort_danger_farms_thread(browser: client, farmlists: list, to_list: int, red: bool, yellow: bool, interval: int) -> None:
    time.sleep(randint(0, 10))
    while True:
        sort_danger_farms(browser, farmlists, to_list, red, yellow)
        time.sleep((interval + randint(0, 10)))
