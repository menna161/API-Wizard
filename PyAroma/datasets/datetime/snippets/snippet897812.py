import os
import json
import pytz
import datetime
import subprocess


def format_datetime(dt, timezone):
    return pytz.timezone(timezone).localize(dt).replace(microsecond=0).isoformat()
