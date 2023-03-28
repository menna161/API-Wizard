import logging
import os
from datetime import datetime, timedelta
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, BotoCoreError
from aws_common_utils_layer import get_session_with_arn, get_session, clear_empty_strings, set_logging_level


def update_recent_cases(support_cases_table, account_id, client, days=DEFAULT_CASE_LOOKBACK_DAYS):
    '\n    Only retrieve updates within last X days to avoid unnecessary duplication\n    '
    kwargs = {'includeResolvedCases': True, 'maxResults': 100, 'afterTime': (datetime.now() - timedelta(days=days)).isoformat()}
    update_cases_helper(support_cases_table, account_id, client, kwargs)
