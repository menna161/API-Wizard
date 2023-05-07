import sys
import re
import random
import time
from multiprocessing import Queue, Pool
from PIL import Image
from douyin import CrawlerScheduler
from common import debug, config, screenshot
from common.auto_adb import auto_adb
from common import apiutil
from common.compression import crop_image


def _random_bias(num):
    '\n    random bias\n    :param num:\n    :return:\n    '
    return random.randint((- num), num)
