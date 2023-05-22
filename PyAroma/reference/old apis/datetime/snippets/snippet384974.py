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


def jobStateChangeEvent(event, JOBTABLE):
    '\n    Process a job state change event and return the updated job data.\n    :param event:  JSON event data struture from Cloudwatch\n    :param JOBTABLE: name of the job data table for this stack\n    '
    progressMetrics = {}
    tsevent = int(datetime.datetime.strptime(event['time'], '%Y-%m-%dT%H:%M:%SZ').timestamp())
    jobId = event['detail']['jobId']
    storedJob = getMediaConvertJob(jobId, JOBTABLE)
    if (storedJob == None):
        job = {}
        job['userMetadata'] = event['detail']['userMetadata']
        job['queue'] = event['detail']['queue']
        job['queueName'] = job['queue'].split('/')[1]
        job['eventTimes'] = {}
        job['eventTimes']['lastTime'] = tsevent
        job['progressMetrics'] = {}
        job['id'] = jobId
        job['createdAt'] = (int((int(event['detail']['timestamp']) / 1000)) - 1)
        job['filters'] = getJobMetricDimensions(job)['filters']
    else:
        job = storedJob
        if ('eventTimes' not in job):
            job['eventTimes'] = {}
        if ('progressMetrics' not in job):
            job['progressMetrics'] = {}
        if (tsevent > job['eventTimes']['lastTime']):
            job['eventTimes']['lastTime'] = tsevent
    if (event['detail']['status'] == 'STATUS_UPDATE'):
        if ((job['eventStatus'] != 'COMPLETE') or (job['status'] != 'COMPLETE')):
            job['eventStatus'] = 'PROGRESSING'
            if (('framesDecoded' not in job['progressMetrics']) or (event['detail']['framesDecoded'] > job['progressMetrics']['framesDecoded'])):
                job['progressMetrics']['framesDecoded'] = event['detail']['framesDecoded']
            if (('lastStatusTime' not in job['eventTimes']) or (tsevent > job['eventTimes']['lastStatusTime'])):
                job['eventTimes']['lastStatusTime'] = tsevent
            job['progressMetrics'] = calculateProgressMetrics(job)
            job['progressMetrics']['percentJobComplete'] = event['detail']['jobProgress']['jobPercentComplete']
            curPhase = event['detail']['jobProgress']['currentPhase']
            job['progressMetrics']['currentPhase'] = curPhase
            job['progressMetrics']['currentPhasePercentComplete'] = event['detail']['jobProgress']['phaseProgress'][curPhase]['percentComplete']
            if (job['progressMetrics']['currentPhase'] == 'TRANSCODING'):
                job['progressMetrics']['percentDecodeComplete'] = event['detail']['jobProgress']['phaseProgress']['TRANSCODING']['percentComplete']
            if (('percentDecodeComplete' in job['progressMetrics']) and (job['progressMetrics']['percentDecodeComplete'] == 100)):
                if ('decodeTime' not in job['eventTimes']):
                    job['eventTimes']['decodeTime'] = tsevent
    elif (event['detail']['status'] == 'PROGRESSING'):
        job['eventStatus'] = 'PROGRESSING'
        if (('status' not in job) or (job['status'] == 'SUBMITTED')):
            job['status'] = 'PROGRESSING'
            job['eventTimes']['firstProgressingTime'] = tsevent
            job['eventTimes']['lastProgressingTime'] = tsevent
        elif (job['status'] == ['PROGRESSING']):
            if (('lastProgressingTime' not in job['eventTimes']) or (job['eventTimes']['lastProgressingTime'] < tsevent)):
                job['eventTimes']['lastProgressingTime'] = tsevent
            if (('firstProgressingTime' not in job['eventTimes']) or (job['eventTimes']['firstProgressingTime'] > tsevent)):
                job['firstProgressingTime'] = tsevent
        job['progressMetrics'] = calculateProgressMetrics(job)
    elif (event['detail']['status'] == 'INPUT_INFORMATION'):
        job['inputDetails'] = event['detail']['inputDetails']
    elif (event['detail']['status'] == 'COMPLETE'):
        job['eventStatus'] = 'COMPLETE'
        job['status'] = 'COMPLETE'
        job['eventTimes']['lastTime'] = tsevent
        job['eventTimes']['completeTime'] = tsevent
        job['eventTimes']['lastProgressingTime'] = tsevent
        job['eventTimes']['lastStatusTime'] = (tsevent + 1)
        if (('analysis' in job) and (job['status'] == 'COMPLETE')):
            job['progressMetrics']['framesDecoded'] = job['analysis']['frameCount']
        job['progressMetrics'] = calculateProgressMetrics(job)
        job['progressMetrics']['percentDecodeComplete'] = 100
        job['progressMetrics']['percentJobComplete'] = 100
        if ('currentPhase' in job['progressMetrics']):
            del job['progressMetrics']['currentPhase']
    elif ((event['detail']['status'] == 'ERROR') or (event['detail']['status'] == 'CANCELED')):
        job['eventStatus'] = event['detail']['status']
        job['status'] = event['detail']['status']
        job['eventTimes']['lastTime'] = tsevent
        job['eventTimes']['errorTime'] = tsevent
        if (job['status'] == 'ERROR'):
            job['progressMetrics'] = calculateProgressMetrics(job)
            if ('percentJobComplete' not in job['progressMetrics']):
                job['progressMetrics']['percentJobComplete'] = 0
        if ('createdAt' not in job):
            job['createdAt'] = int((int(event['detail']['timestamp']) / 1000))
    return job
