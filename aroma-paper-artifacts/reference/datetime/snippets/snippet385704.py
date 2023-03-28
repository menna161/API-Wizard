import boto3
import sys
from datetime import date, datetime, timedelta
import hashlib
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import argparse
import datetime


def list_reserved_instances(filters):
    events = []
    instances = []
    event_ids = []
    client = boto3.client('ec2')
    response = client.describe_reserved_instances(Filters=filters)
    size = len(response.get('ReservedInstances'))
    columns_format = '%-36s %-10s %-12s %-24s %-18s %-14s %-10s %-9s %-26s %-6s'
    print((columns_format % ('Reserved Id', 'Instances', 'Type', 'Product Description', 'Scope', 'Zone', 'Duration', 'Time Left', 'End', 'Offering')))
    for n in range(size):
        id = response.get('ReservedInstances')[n].get('ReservedInstancesId')
        count = response.get('ReservedInstances')[n].get('InstanceCount')
        type = response.get('ReservedInstances')[n].get('InstanceType')
        product = response.get('ReservedInstances')[n].get('ProductDescription')
        scope = response.get('ReservedInstances')[n].get('Scope')
        zone = response.get('ReservedInstances')[n].get('AvailabilityZone')
        duration = response.get('ReservedInstances')[n].get('Duration')
        offering = response.get('ReservedInstances')[n].get('OfferingType')
        td = timedelta(seconds=int(duration))
        end = response.get('ReservedInstances')[n].get('End')
        end_dt = datetime.strptime(str(end), '%Y-%m-%d %H:%M:%S+00:00')
        now_dt = datetime.now()
        delta = (end_dt - now_dt)
        time_left = max(0, delta.days)
        print((columns_format % (id, count, type, product, scope, zone, td.days, time_left, end, offering)))
        description = ('A purchased reservervation affecting to %s x %s instances is about to expire. Reservation id: %s' % (count, type, id))
        if (time_left > 0):
            state = 'active'
        else:
            state = 'retired'
        instance = {'scope': scope, 'zone': zone, 'type': type, 'state': state, 'count': count}
        instances.append(instance)
        event_start = end_dt.strftime('%Y-%m-%dT%H:%M:%S+00:00')
        event_end = (end_dt + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S+00:00')
        m = hashlib.sha224()
        m.update(id.encode())
        sha_id = m.hexdigest()
        event = {'id': sha_id, 'summary': 'Reserve Instance Expiration', 'location': 'aws', 'description': description, 'start': {'dateTime': event_start, 'timeZone': 'America/Los_Angeles'}, 'end': {'dateTime': event_end, 'timeZone': 'America/Los_Angeles'}, 'reminders': {'useDefault': False, 'overrides': [{'method': 'email', 'minutes': (24 * 60)}, {'method': 'popup', 'minutes': 10}]}}
        events.append(event)
        event_ids.append(sha_id)
    return (events, event_ids, instances)
