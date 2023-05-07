import re
import sys
import requests
from time import sleep
from shodan import Shodan
from datetime import datetime
from threading import Thread, activeCount


def getTime():
    now = datetime.now()
    return now.strftime('%H:%M:%S')
