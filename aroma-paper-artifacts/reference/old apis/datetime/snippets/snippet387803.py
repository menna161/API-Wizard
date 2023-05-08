import os
import pytest
import time
import datetime
from azure import eventhub
from azure.eventhub import EventData, EventHubClient, Offset


def test_receive_with_datetime_sync(connstr_senders):
    (connection_str, senders) = connstr_senders
    client = EventHubClient.from_connection_string(connection_str, debug=False)
    partitions = client.get_eventhub_info()
    assert (partitions['partition_ids'] == ['0', '1'])
    receiver = client.add_receiver('$default', '0', offset=Offset('@latest'))
    try:
        client.run()
        more_partitions = client.get_eventhub_info()
        assert (more_partitions['partition_ids'] == ['0', '1'])
        received = receiver.receive(timeout=5)
        assert (len(received) == 0)
        senders[0].send(EventData(b'Data'))
        received = receiver.receive(timeout=5)
        assert (len(received) == 1)
        offset = received[0].enqueued_time
        assert (list(received[0].body) == [b'Data'])
        assert (received[0].body_as_str() == 'Data')
        offset_receiver = client.add_receiver('$default', '0', offset=Offset(offset))
        client.run()
        received = offset_receiver.receive(timeout=5)
        assert (len(received) == 0)
        senders[0].send(EventData(b'Message after timestamp'))
        received = offset_receiver.receive(timeout=5)
        assert (len(received) == 1)
    except:
        raise
    finally:
        client.stop()
