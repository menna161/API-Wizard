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


def _get_last_chromium_modification():
    'Returns the last modification date of the chromium-browser-official tar file'
    with _get_requests_session() as session:
        response = session.head('https://storage.googleapis.com/chromium-browser-official/chromium-{}.tar.xz'.format(get_chromium_version()))
        response.raise_for_status()
        return email.utils.parsedate_to_datetime(response.headers['Last-Modified'])
