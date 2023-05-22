import datetime
import json
import logging
from salt.returners import get_returner_options
import paho.mqtt.client as mqtt
import ssl


def returner_data(data, *args, **kwargs):
    '\n    Return any arbitrary data structure to MQTT.\n    '
    if (not data):
        log.debug('Skipping empty data result')
        return
    namespace = list(args)
    if isinstance(data, dict):
        payload = data
        if (('_type' in data) and (not (data['_type'] in namespace))):
            namespace.append(data['_type'])
    elif isinstance(data, (list, set, tuple)):
        payload = {'_stamp': datetime.datetime.utcnow().isoformat(), 'values': data}
    else:
        payload = {'_stamp': datetime.datetime.utcnow().isoformat(), 'value': data}
    client = _get_client_for(kwargs)
    topic = '/'.join(namespace)
    res = client.publish(topic, json.dumps(payload, separators=(',', ':')))
    if (res.rc != mqtt.MQTT_ERR_SUCCESS):
        log.warn("Publish of message with topic '{:}' failed: {:}".format(topic, mqtt.error_string(res.rc)))
