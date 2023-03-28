import argparse
import boto3
import sys
import re
import os
import time
import json
import logging
from datetime import datetime
from collections import defaultdict


def dump_stats(stats, arn):
    ' Check and log run statistics, notify SNS if ARN is defined\n\n    Args:\n        stats: statistics dict\n\n    Returns:\n        int: 0 for success, non-zero otherwise\n    '
    total = (stats['total_errors'] + stats['snap_errors'])
    if (total > 0):
        exitcode = 3
        logstats = log.error
        subj = 'Error making snapshots'
    else:
        exitcode = 0
        logstats = log.info
        subj = 'Completed making snapshots'
    stat = ['']
    stat.append('Finished making snapshots at {} for {} volume(s), {} errors'.format(datetime.today().strftime('%d-%m-%Y %H:%M:%S'), stats['total_vols'], total))
    stat.append('Created: {}, deleted: {}, errors: {}'.format(stats['snap_creates'], stats['snap_deletes'], stats['snap_errors']))
    for s in stat:
        logstats(s)
    if arn:
        try:
            log.info('Notify SNS: %s', arn)
            sns = boto3.client('sns')
            sns.publish(TopicArn=arn, Subject=subj, Message='\n'.join(stat))
        except Exception as err:
            log.error(("Can't notify ARN:" + str(sys.exc_info()[0])))
            log.error(err)
            exitcode = 4
            pass
    return exitcode
