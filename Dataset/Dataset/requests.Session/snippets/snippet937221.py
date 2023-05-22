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


def _initialize_deps_tree():
    "\n    Initializes and returns a dependency tree for DEPS files\n\n    The DEPS tree is a dict has the following format:\n    key - pathlib.Path relative to the DEPS file's path\n    value - tuple(repo_url, version, recursive dict here)\n        repo_url is the URL to the dependency's repository root\n        If the recursive dict is a string, then it is a string to the DEPS file to load\n            if needed\n\n    download_session is an active requests.Session() object\n    "
    root_deps_tree = {_SRC_PATH: ('https://chromium.googlesource.com/chromium/src.git', get_chromium_version(), 'DEPS')}
    return root_deps_tree
