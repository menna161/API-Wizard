from .custom_driver import client, use_browser
import time
from random import randint
from .utils import log
from .village import open_village, open_city, open_building
from .farming import send_farm
from .util_game import close_modal, shortcut, open_shortcut, check_resources, old_shortcut
from .settings import settings
import json


def check_for_attack_thread(browser: client, village: int, interval: int, units: list, target: list, save_resources: bool, units_train: list) -> None:
    time.sleep(randint(0, 10))
    if save_resources:
        with open(settings.units_path, 'r') as f:
            content = json.load(f)
    while True:
        sleep_time = interval
        attack_time = check_for_attack(browser, village)
        if attack_time:
            timelist = attack_time.split(':')
            countdown = ((((int(timelist[0]) * 60) * 60) + (int(timelist[1]) * 60)) + int(timelist[0]))
            save_send_time = (10 * 60)
            if (countdown < save_send_time):
                unit_dict = {}
                for unit in units:
                    unit_dict[int(unit)] = (- 1)
                send_farm(browser=browser, village=village, units=unit_dict, x=int(target[0]), y=int(target[1]))
                log('units sent to rescue')
                if save_resources:
                    save_resources_gold(browser, units_train, content)
                sleep_time = save_send_time
            elif (countdown > (sleep_time + save_send_time)):
                pass
            else:
                sleep_time = (countdown - (save_send_time - 10))
            pass
        time.sleep(sleep_time)
