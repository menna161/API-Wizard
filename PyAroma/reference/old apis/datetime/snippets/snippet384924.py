import boto3
import datetime
import json
import time
import decimal
from botocore.client import ClientError
from boto3 import resource
from boto3.dynamodb.conditions import Key
import os
import traceback


def lambda_handler(event, context):
    print(json.dumps(event))
    job = {}
    tsevent = int(datetime.datetime.strptime(event['time'], '%Y-%m-%dT%H:%M:%SZ').timestamp())
    try:
        EVENTTABLE = os.environ['EventTable']
        EVENTTABLETTL = os.environ['EventTableTTL']
        EVENT_RETENTION_PERIOD = ((3600 * 24) * int(EVENTTABLETTL))
        event['timestamp'] = tsevent
        event['timestampTTL'] = (tsevent + EVENT_RETENTION_PERIOD)
        event['jobId'] = event['detail']['jobId']
        s = json.dumps(event, cls=DecimalEncoder)
        event = json.loads(s, parse_float=decimal.Decimal)
        table = DYNAMO_CLIENT.Table(EVENTTABLE)
        response = table.put_item(Item=event)
        print(json.dumps(response, cls=DecimalEncoder))
    except Exception as e:
        print('An error occured {}'.format(e))
        traceback.print_stack()
        raise
    else:
        return True
