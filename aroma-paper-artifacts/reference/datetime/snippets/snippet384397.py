import datetime
import gzip
import json
import logging
import sys
import time
from argparse import ArgumentParser
import boto3
from botocore.client import Config
import elastic
from configservice_util import ConfigServiceUtil


def main(args, es):
    iso_now_time = datetime.datetime.now().isoformat()
    app_log.info(('Snapshot Time: ' + str(iso_now_time)))
    region = args.region
    es.set_not_analyzed_template()
    my_regions = []
    if (region is not None):
        my_regions.append(region)
    else:
        my_regions = REGIONS
    verbose_log.info('Looping through the regions')
    for curRegion in my_regions:
        loop_through_regions(curRegion, iso_now_time, es)
