import base64
import boto3
import json
import logging
import os
from botocore.exceptions import ClientError
from datetime import datetime, timezone, timedelta


def convert_iso_format(timestamp: int) -> str:
    tz = timezone(timedelta(hours=9))
    timestamp = datetime.fromtimestamp((timestamp / 1000), tz)
    return timestamp.isoformat(timespec='milliseconds')
