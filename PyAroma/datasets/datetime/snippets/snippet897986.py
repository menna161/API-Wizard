import pytest
import datetime
from pupa.scrape import Event


def event_obj():
    e = Event(name='get-together', start_date=(datetime.datetime.utcnow().isoformat().split('.')[0] + 'Z'), location_name="Joe's Place")
    e.add_source(url='http://example.com/foobar')
    return e
