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


def _get_gitiles_git_log_date(log_entry):
    'Helper for _get_gitiles_git_log_date'
    return email.utils.parsedate_to_datetime(log_entry['committer']['time'])
