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


def _download_source_file(download_session, root_deps_tree, fallback_repo_manager, target_file):
    '\n    Downloads the source tree file from googlesource.com\n\n    download_session is an active requests.Session() object\n    deps_dir is a pathlib.Path to the directory containing a DEPS file.\n    '
    (current_node, current_relative_path) = _get_target_file_deps_node(download_session, root_deps_tree, target_file)
    (repo_url, version, _) = current_node
    try:
        return _download_googlesource_file(download_session, repo_url, version, current_relative_path)
    except _NotInRepoError:
        pass
    get_logger().debug('Path "%s" (relative: "%s") not found using DEPS tree; finding fallback repo...', target_file, current_relative_path)
    (repo_url, version, current_relative_path) = fallback_repo_manager.get_fallback(current_relative_path, current_node, root_deps_tree)
    if (not repo_url):
        get_logger().error('No fallback repo found for "%s" (relative: "%s")', target_file, current_relative_path)
        raise _NotInRepoError()
    try:
        return _download_googlesource_file(download_session, repo_url, version, current_relative_path)
    except _NotInRepoError:
        pass
    get_logger().error('File "%s" (relative: "%s") not found in fallback repo "%s", version "%s"', target_file, current_relative_path, repo_url, version)
    raise _NotInRepoError()
