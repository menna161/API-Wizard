from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import selenium.common.exceptions
import time, datetime, platform
import getpass


def course_timer(hour, minute):
    if ((hour > 23) or (hour < 0)):
        hour %= 24
    if ((minute > 59) or (minute < 0)):
        minute %= 60
    now = datetime.datetime.now()
    course_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if (now >= course_time):
        return True
    return False
