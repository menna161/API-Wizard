import os
import pytest
import time
import datetime
from azure import eventhub
from azure.eventhub import EventData, EventHubClient, Offset


def test_receive_with_custom_datetime_sync(connstr_senders):
    (connection_str, senders) = connstr_senders
    client = EventHubClient.from_connection_string(connection_str, debug=False)
    for i in range(5):
        senders[0].send(EventData(b'Message before timestamp'))
    time.sleep(60)
    now = datetime.datetime.utcnow()
    offset = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
    for i in range(5):
        senders[0].send(EventData(b'Message after timestamp'))
    receiver = client.add_receiver('$default', '0', offset=Offset(offset))
    try:
        client.run()
        all_received = []
        received = receiver.receive(timeout=1)
        while received:
            all_received.extend(received)
            received = receiver.receive(timeout=1)
        assert (len(all_received) == 5)
        for received_event in all_received:
            assert (received_event.body_as_str() == 'Message after timestamp')
            assert (received_event.enqueued_time > offset)
    except:
        raise
    finally:
        client.stop()
