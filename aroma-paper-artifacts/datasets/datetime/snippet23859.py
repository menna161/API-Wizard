import asyncio
import datetime
import json
import threading
import pytest
from google.cloud import pubsub
from google.cloud import pubsub_v1
from gordon import interfaces
from gordon_gcp import exceptions
from gordon_gcp.plugins.service import event_consumer
from gordon_gcp.schema import parse
from gordon_gcp.schema import validate
from tests.unit import conftest


@pytest.fixture
def publish_time():
    return datetime.datetime(2018, 1, 1, 11, 30, 0, tzinfo=datetime.timezone.utc)
