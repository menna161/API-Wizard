import argparse
import ast
import base64
import email.utils
import json
import logging
import sys
import tempfile
from pathlib import Path
import unidiff
from unidiff.constants import LINE_TYPE_EMPTY, LINE_TYPE_NO_NEWLINE
from domain_substitution import TREE_ENCODINGS
from _common import ENCODING, get_logger, get_chromium_version, parse_series, add_common_params
from patches import dry_run_check
import requests
import requests.adapters
import urllib3.util


def _get_requests_session():
    session = requests.Session()
    http_adapter = requests.adapters.HTTPAdapter(max_retries=_VerboseRetry(total=10, read=10, connect=10, backoff_factor=8, status_forcelist=urllib3.Retry.RETRY_AFTER_STATUS_CODES, raise_on_status=False))
    session.mount('http://', http_adapter)
    session.mount('https://', http_adapter)
    return session
