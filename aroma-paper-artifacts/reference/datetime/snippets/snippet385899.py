import base64
import datetime
import json
import sys
import time
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import get_credentials
from botocore.endpoint import BotocoreHTTPSession
from botocore.session import Session
from src.common.encoder import StreamTypeDeserializer
from src.common.exceptions import ESException
from src.common.log import get_logger
import urllib
import urlparse
import urllib.request as urllib
import urllib.parse as urlparse


def execute(self):
    records = self.event['Records']
    now = datetime.datetime.utcnow()
    ddb_deserializer = StreamTypeDeserializer()
    es_actions = []
    cnt_insert = cnt_modify = cnt_remove = 0
    for record in records:
        if (record.get('eventSource') == 'aws:dynamodb'):
            ddb = record['dynamodb']
            ddb_table_name = self.get_table_name_from_arn(record['eventSourceARN'])
            doc_seq = ddb['SequenceNumber']
        elif (record.get('eventSource') == 'aws:kinesis'):
            ddb = json.loads(base64.b64decode(record['kinesis']['data']))
            ddb_table_name = ddb['SourceTable']
            doc_seq = record['kinesis']['sequenceNumber']
        else:
            get_logger().error('Ignoring non-DynamoDB event sources: %s', record.get('eventSource'))
            continue
        doc_table = self.doc_type_format.format(ddb_table_name.lower())
        doc_type = self.doc_type_format.format(ddb_table_name.lower())
        doc_index = self.compute_doc_index(ddb['Keys'], ddb_deserializer)
        event_name = record['eventName'].upper()
        if (event_name == 'AWS:KINESIS:RECORD'):
            event_name = 'INSERT'
        if (event_name == 'INSERT'):
            cnt_insert += 1
        elif (event_name == 'MODIFY'):
            cnt_modify += 1
        elif (event_name == 'REMOVE'):
            cnt_remove += 1
        else:
            get_logger().warning('Unsupported event_name: %s', event_name)
        if ((event_name == 'INSERT') or (event_name == 'MODIFY')):
            if ('NewImage' not in ddb):
                get_logger().warning('Cannot process stream if it does not contain NewImage')
                continue
            doc_fields = ddb_deserializer.deserialize({'M': ddb['NewImage']})
            doc_fields['@timestamp'] = now.isoformat()
            doc_fields['@SequenceNumber'] = doc_seq
            doc_json = json.dumps(doc_fields)
            action = {'index': {'_index': doc_table, '_type': doc_type, '_id': doc_index}}
            es_actions.append(json.dumps(action))
            es_actions.append(doc_json)
        elif (event_name == 'REMOVE'):
            action = {'delete': {'_index': doc_table, '_type': doc_type, '_id': doc_index}}
            es_actions.append(json.dumps(action))
    es_actions.append('')
    es_payload = '\n'.join(es_actions)
    self.post_to_es(es_payload)
