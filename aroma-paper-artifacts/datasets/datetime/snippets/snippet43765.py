import datetime
import pytest
from hive.utils.normalize import parse_time
from hive.steem.client import SteemClient


def test_head_time(client):
    head = parse_time(client.head_time())
    assert (head > (datetime.datetime.now() - datetime.timedelta(minutes=15)))
