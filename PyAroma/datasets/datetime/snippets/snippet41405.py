import boto3
import datetime
import json
import time
import decimal
from botocore.client import ClientError
from boto3 import resource
from boto3.dynamodb.conditions import Key
import logging
import subprocess
from urllib.parse import urlparse
import timecode
from timecode import Timecode
import xmltodict
import logging
import os
import traceback


def lambda_handler(event, context):
    "\n    Event collector for mediaconvert event type.  Events are cleaned to ensure they\n    have the minimum consistent schema.  The collector maintains a persistent job object \n    in dydnamodb that it updates as events occur.  Since events may arrive out of order from the \n    time they are generated, we need to be careful about overwriting newer information\n    with older information.  \n    Each event should carry at least these key value pairs:\n    \n    'MediaConvertCollecterEvent': { \n    'time': timestamp,\n    'detail': {\n        'eventName': 'MediaConvert Job State Change'\n        'status': '[SUBMITTED, PROGRESSING, INPUT_INFORMATION,STATUS_UPDATE, COMPLETE, ERROR]',\n        'jobId': 'jobId',\n        'queue': `queue ARN`,\n        'userMetadata': {'key1': 'value1', ...}\n        } \n    }\n    "
    print(json.dumps(event))
    job = {}
    tsevent = int(datetime.datetime.strptime(event['time'], '%Y-%m-%dT%H:%M:%SZ').timestamp())
    try:
        JOBTABLE = os.environ['JobTable']
        JOBTABLETTL = os.environ['JobTableTTL']
        JOBSTREAM = os.environ['JobStream']
        EVENTTABLE = os.environ['EventTable']
        EVENTTABLETTL = os.environ['EventTableTTL']
        EVENTSTREAM = os.environ['EventStream']
        METRICSTREAM = os.environ['MetricStream']
        JOB_RETENTION_PERIOD = ((3600 * 24) * int(JOBTABLETTL))
        EVENT_RETENTION_PERIOD = ((3600 * 24) * int(EVENTTABLETTL))
        if ((event['detail-type'] == 'AWS API Call via CloudTrail') and (event['detail']['eventName'] == 'CreateJob')):
            job = jobCreateEvent(event, JOBTABLE)
        elif (event['detail-type'] == 'MediaConvert Job State Change'):
            job = jobStateChangeEvent(event, JOBTABLE)
        else:
            print(('Unrecognized event! ' + event['detail-type']))
            return False
        job['timestamp'] = job['eventTimes']['lastTime']
        job['timestampTTL'] = (tsevent + JOB_RETENTION_PERIOD)
        s = json.dumps(job, cls=DecimalEncoder)
        job = json.loads(s, parse_float=decimal.Decimal)
        table = DYNAMO_CLIENT.Table(JOBTABLE)
        response = table.put_item(Item=job)
        print(json.dumps(response, cls=DecimalEncoder))
        event['timestamp'] = tsevent
        event['testTime'] = tsevent
        event['timestampTTL'] = (tsevent + EVENT_RETENTION_PERIOD)
        event['jobId'] = job['id']
        s = json.dumps(event, cls=DecimalEncoder)
        event = json.loads(s, parse_float=decimal.Decimal)
        table = DYNAMO_CLIENT.Table(EVENTTABLE)
        response = table.put_item(Item=event)
        print(json.dumps(response, cls=DecimalEncoder))
        print('Push Job to Kinesis')
        response = KINESIS_CLIENT.put_record(StreamName=JOBSTREAM, Data=json.dumps(job, cls=DecimalEncoder), PartitionKey=job['id'])
        print(json.dumps(response, default=str))
        response = KINESIS_CLIENT.put_record(StreamName=EVENTSTREAM, Data=json.dumps(event, cls=DecimalEncoder), PartitionKey=event['id'])
        print(json.dumps(response, default=str))
        putProgressMetrics(job, job['eventTimes']['lastTime'], METRICSTREAM)
        putStatusMetrics(job, tsevent, job['eventStatus'], METRICSTREAM)
    except Exception as e:
        print('An error occured {}'.format(e))
        traceback.print_stack()
        raise
    else:
        return True
