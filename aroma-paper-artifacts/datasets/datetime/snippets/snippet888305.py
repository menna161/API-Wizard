import datetime
import logging
import os
import boto3


def handler(_event, _context):
    logging.debug('environment variables:\n %s', os.environ)
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    timestamp = (timestamp - datetime.timedelta(minutes=((timestamp.minute % 5) + 10), seconds=timestamp.second, microseconds=timestamp.microsecond))
    logging.info('evaluating at [%s]', timestamp)
    metrics = get_metrics(timestamp)
    logging.debug('available metrics: %s', metrics)
    messages = metrics['maxANOMV']
    requests = metrics['sumNOER']
    machines = metrics['avgGISI']
    logging.info('ANOMV=%s NOER=%s GISI=%s', messages, requests, machines)
    if (machines > 0):
        load = (1.0 - (requests / ((machines * 0.098444) * 300)))
    elif (messages > 0):
        load = 1.0
    else:
        return
    logging.info('L=%s', load)
    put_metric(timestamp, load)
