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


def find_candidates(self, project_name, specifier=None):
    'Find matches for the given project and specifier.\n\n        If given, `specifier` should implement `filter` to allow version\n        filtering (e.g. ``packaging.specifiers.SpecifierSet``).\n\n        Returns a `FoundCandidates` instance.\n        '
    if (specifier is None):
        specifier = specifiers.SpecifierSet()
    return FoundCandidates.from_specifier(self.find_all_candidates(project_name), specifier=specifier, prereleases=(self.allow_all_prereleases or None), evaluator=self.candidate_evaluator)
