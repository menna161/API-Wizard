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


def _get_gitiles_commit_before_date(repo_url, target_branch, target_datetime):
    'Returns the hexadecimal hash of the closest commit before target_datetime'
    json_log_url = '{repo}/+log/{branch}?format=JSON'.format(repo=repo_url, branch=target_branch)
    with _get_requests_session() as session:
        response = session.get(json_log_url)
        response.raise_for_status()
        git_log = json.loads(response.text[5:])
    assert (len(git_log) == 2)
    assert ('log' in git_log)
    assert git_log['log']
    git_log = git_log['log']
    if (_get_gitiles_git_log_date(git_log[0]) < target_datetime):
        return git_log[0]['commit']
    if (_get_gitiles_git_log_date(git_log[(- 1)]) > target_datetime):
        get_logger().warning('Oldest entry in gitiles log for repo "%s" is newer than target; continuing with oldest entry...')
        return git_log[(- 1)]['commit']
    low_index = 0
    high_index = (len(git_log) - 1)
    mid_index = high_index
    while (low_index != high_index):
        mid_index = (low_index + ((high_index - low_index) // 2))
        if (_get_gitiles_git_log_date(git_log[mid_index]) > target_datetime):
            low_index = (mid_index + 1)
        else:
            high_index = mid_index
    return git_log[mid_index]['commit']
