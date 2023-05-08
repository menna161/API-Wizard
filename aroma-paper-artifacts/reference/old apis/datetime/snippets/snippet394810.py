import concurrent.futures
import contextlib
import contextvars
import dataclasses
import hashlib
import logging
import os
import platform
import sys
import typing
import uuid
from datetime import datetime
from functools import wraps
from os.path import expanduser, join
from pathlib import Path
import requests
from feast import flags_helper
from feast.constants import DEFAULT_FEAST_USAGE_VALUE, FEAST_USAGE
from feast.version import get_version


def _set_installation_id():
    if os.getenv('FEAST_FORCE_USAGE_UUID'):
        _constant_attributes['installation_id'] = os.getenv('FEAST_FORCE_USAGE_UUID')
        _constant_attributes['installation_ts'] = datetime.utcnow().isoformat()
        return
    feast_home_dir = join(expanduser('~'), '.feast')
    installation_timestamp = datetime.utcnow()
    try:
        Path(feast_home_dir).mkdir(exist_ok=True)
        usage_filepath = join(feast_home_dir, 'usage')
        if os.path.exists(usage_filepath):
            installation_timestamp = datetime.utcfromtimestamp(os.path.getmtime(usage_filepath))
            with open(usage_filepath, 'r') as f:
                installation_id = f.read()
        else:
            installation_id = str(uuid.uuid4())
            with open(usage_filepath, 'w') as f:
                f.write(installation_id)
            print('Feast is an open source project that collects anonymized error reporting and usage statistics. To opt out or learn more see https://docs.feast.dev/reference/usage')
    except OSError as e:
        _logger.debug(f'Unable to configure usage {e}')
        installation_id = 'undefined'
    _constant_attributes['installation_id'] = installation_id
    _constant_attributes['installation_ts'] = installation_timestamp.isoformat()
