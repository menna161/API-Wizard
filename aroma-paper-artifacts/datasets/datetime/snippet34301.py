import sys
from abc import ABC, abstractmethod
from datetime import datetime
import requests
from persistence import BookmarkDatabase


def execute(self, data, timestamp=None):
    data['date_added'] = (timestamp or datetime.utcnow().isoformat())
    persistence.create(data)
    return (True, None)
