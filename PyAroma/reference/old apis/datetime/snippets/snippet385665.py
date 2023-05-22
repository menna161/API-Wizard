import json
import math
import os
import time
from datetime import datetime
from uuid import uuid4
from model import table
from scheduler import schedule_events
from sns_client import publish_sns


def get_seconds_remaining(date):
    now = datetime.utcnow()
    target = datetime.fromisoformat(date)
    delta = (target - now)
    return math.ceil(delta.total_seconds())
