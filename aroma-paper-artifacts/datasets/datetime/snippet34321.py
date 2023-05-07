import sys
from abc import ABC, abstractmethod
from datetime import datetime
import requests
from database import DatabaseManager


def execute(self, data, timestamp=None):
    data['date_added'] = (timestamp or datetime.utcnow().isoformat())
    db.add('bookmarks', data)
    return (True, None)
