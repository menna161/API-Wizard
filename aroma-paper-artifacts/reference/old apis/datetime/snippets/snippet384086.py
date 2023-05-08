import argparse
from datetime import datetime, timedelta
from dateutil import tz
from time import sleep
import boto3


def delete_old_streams(log_group, dry_run=False):
    "\n    Delete old log streams that are empty. Events get cleaned up by log_group['retentionInDays'] but the streams don't.\n    "
    print_log_group(log_group, 'Checking for old streams...')
    now = datetime.utcnow().replace(tzinfo=tz.tzutc())
    if ('retentionInDays' in log_group):
        oldest_valid_event = (now - timedelta(days=log_group['retentionInDays']))
    else:
        print_log_group(log_group, 'Log Group has no expiration set, skipping.')
        return
    print((' - Streams in group: ' + log_group['logGroupName']))
    for stream in get_streams(log_group):
        if ('lastEventTimestamp' in stream):
            stream_time = datetime.fromtimestamp((stream['lastEventTimestamp'] / 1000), tz=tz.tzutc())
        else:
            stream_time = datetime.fromtimestamp((stream['creationTime'] / 1000), tz=tz.tzutc())
        if (stream_time < oldest_valid_event):
            if dry_run:
                print_log_group(log_group, (('Would delete stream: ' + stream['logStreamName']) + ' (--dry-run set)'))
            else:
                print_log_group(log_group, ('Deleting stream: ' + stream['logStreamName']))
                client.delete_log_stream(logGroupName=log_group['logGroupName'], logStreamName=stream['logStreamName'])
                print_log_group(log_group, ('Deleted stream: ' + stream['logStreamName']))
                sleep(0.2)
        else:
            print_log_group(log_group, ('Checked stream, keeping: ' + stream['logStreamName']))
