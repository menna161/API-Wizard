import datetime
import subprocess
from time import sleep
import random
from pocket_api import Pocket, RateLimitException
from workflow import Workflow, PasswordNotFound
from workflow.background import run_in_background, is_running
from pocket_errors import ERROR_MESSAGES
import config


def get_subtitle(item_count, time_updated, given_url, tags=None):
    time_updated = datetime.datetime.fromtimestamp(int(time_updated)).strftime('%Y-%m-%d %H:%M')
    short_url = given_url.replace('http://', '').replace('https://', '')
    subtitle_elements = [('#%s' % item_count), time_updated, short_url]
    if tags:
        tags = [('#%s' % x) for x in tags.keys()]
        subtitle_elements.insert(2, ', '.join(tags))
    return ' - '.join(subtitle_elements)
