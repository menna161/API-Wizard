from __future__ import absolute_import
import cgi
import itertools
import logging
import mimetypes
import os
import posixpath
import re
import sys
from collections import namedtuple
from pip._vendor import html5lib, requests, six
from pip._vendor.distlib.compat import unescape
from pip._vendor.packaging import specifiers
from pip._vendor.packaging.utils import canonicalize_name
from pip._vendor.packaging.version import parse as parse_version
from pip._vendor.requests.exceptions import HTTPError, RetryError, SSLError
from pip._vendor.six.moves.urllib import parse as urllib_parse
from pip._vendor.six.moves.urllib import request as urllib_request
from pip._internal.download import HAS_TLS, is_url, path_to_url, url_to_path
from pip._internal.exceptions import BestVersionAlreadyInstalled, DistributionNotFound, InvalidWheelFilename, UnsupportedWheel
from pip._internal.models.candidate import InstallationCandidate
from pip._internal.models.format_control import FormatControl
from pip._internal.models.index import PyPI
from pip._internal.models.link import Link
from pip._internal.pep425tags import get_supported
from pip._internal.utils.compat import ipaddress
from pip._internal.utils.logging import indent_log
from pip._internal.utils.misc import ARCHIVE_EXTENSIONS, SUPPORTED_EXTENSIONS, WHEEL_EXTENSION, normalize_path, redact_password_from_url
from pip._internal.utils.packaging import check_requires_python
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.wheel import Wheel
from logging import Logger
from typing import Tuple, Optional, Any, List, Union, Callable, Set, Sequence, Iterable, MutableMapping
from pip._vendor.packaging.version import _BaseVersion
from pip._vendor.requests import Response
from pip._internal.pep425tags import Pep425Tag
from pip._internal.req import InstallRequirement
from pip._internal.download import PipSession
from pip._internal.vcs import VcsSupport


def find_all_candidates(self, project_name):
    'Find all available InstallationCandidate for project_name\n\n        This checks index_urls and find_links.\n        All versions found are returned as an InstallationCandidate list.\n\n        See _link_package_versions for details on which files are accepted\n        '
    index_locations = self._get_index_urls_locations(project_name)
    (index_file_loc, index_url_loc) = self._sort_locations(index_locations)
    (fl_file_loc, fl_url_loc) = self._sort_locations(self.find_links, expand_dir=True)
    file_locations = (Link(url) for url in itertools.chain(index_file_loc, fl_file_loc))
    url_locations = [link for link in itertools.chain((Link(url) for url in index_url_loc), (Link(url) for url in fl_url_loc)) if self._validate_secure_origin(logger, link)]
    logger.debug('%d location(s) to search for versions of %s:', len(url_locations), project_name)
    for location in url_locations:
        logger.debug('* %s', location)
    canonical_name = canonicalize_name(project_name)
    formats = self.format_control.get_allowed_formats(canonical_name)
    search = Search(project_name, canonical_name, formats)
    find_links_versions = self._package_versions((Link(url, '-f') for url in self.find_links), search)
    page_versions = []
    for page in self._get_pages(url_locations, project_name):
        logger.debug('Analyzing links from page %s', page.url)
        with indent_log():
            page_versions.extend(self._package_versions(page.iter_links(), search))
    file_versions = self._package_versions(file_locations, search)
    if file_versions:
        file_versions.sort(reverse=True)
        logger.debug('Local files found: %s', ', '.join([url_to_path(candidate.location.url) for candidate in file_versions]))
    return ((file_versions + find_links_versions) + page_versions)
