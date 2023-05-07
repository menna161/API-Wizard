import sys
from datetime import datetime
import requests
from database import DatabaseManager


def execute(self, data, timestamp=None):
    data['date_added'] = (timestamp or datetime.utcnow().isoformat())
    db.add('bookmarks', data)
    return 'Bookmark added!'
