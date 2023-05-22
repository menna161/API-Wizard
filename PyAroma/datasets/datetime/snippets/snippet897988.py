import pytest
import datetime
from pupa.scrape import Event


def test_no_location():
    e = Event(name='get-together', start_date=(datetime.datetime.utcnow().isoformat().split('.')[0] + 'Z'))
    e.add_source(url='http://example.com/foobar')
    e.validate()
