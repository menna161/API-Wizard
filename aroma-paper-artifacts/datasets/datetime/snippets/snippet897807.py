import os
import json
import pytz
import datetime
import subprocess


def utcnow():
    return datetime.datetime.now(datetime.timezone.utc)
