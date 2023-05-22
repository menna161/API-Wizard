import pytest
from datetime import datetime, timedelta
from random import choice, randrange
from athena_glue_service_logs.cloudtrail import CloudTrailRawCatalog, CloudTrailConvertedCatalog
from utils import GlueStubber


def build_glue_response(num, next_token=None):
    'Helper to programatically create a Glue API response'
    available_regions = ['ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3', 'ap-south-1', 'ap-southeast-1', 'ap-southeast-2', 'ca-central-1', 'eu-central-1', 'eu-north-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'sa-east-1', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']
    response = {'Partitions': []}
    if (next_token is not None):
        response['NextToken'] = next_token
    start_date = datetime.utcnow().date()
    part_date = start_date
    for i in range(num):
        part = ([choice(available_regions)] + part_date.strftime('%Y-%m-%d').split('-'))
        part_date = (part_date + timedelta(days=(- randrange(30))))
        response['Partitions'].append({'Values': part})
    return response
