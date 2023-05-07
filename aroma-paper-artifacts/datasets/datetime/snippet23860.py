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
def pubsub_msg(mocker, raw_msg_data, publish_time):
    mocker.patch(DATETIME_PATCH, conftest.MockDatetime)
    pubsub_msg = mocker.MagicMock(pubsub_v1.subscriber.message.Message)
    pubsub_msg.message_id = 1234
    pubsub_msg.data = bytes(json.dumps(raw_msg_data), encoding='utf-8')
    pubsub_msg.publish_time = datetime.datetime.now(datetime.timezone.utc)
    return pubsub_msg
