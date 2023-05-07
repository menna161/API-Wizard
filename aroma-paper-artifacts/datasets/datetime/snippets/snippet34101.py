import sys
from datetime import datetime
from database import DatabaseManager


def execute(self, data):
    data['date_added'] = datetime.utcnow().isoformat()
    db.add('bookmarks', data)
    return 'Bookmark added!'
