from __future__ import absolute_import
import logging
import re
from pip._vendor.packaging import specifiers
from pip._vendor.packaging.utils import canonicalize_name
from pip._vendor.packaging.version import parse as parse_version
from pip._internal.exceptions import BestVersionAlreadyInstalled, DistributionNotFound, InvalidWheelFilename, UnsupportedWheel
from pip._internal.index.collector import parse_links
from pip._internal.models.candidate import InstallationCandidate
from pip._internal.models.format_control import FormatControl
from pip._internal.models.link import Link
from pip._internal.models.selection_prefs import SelectionPreferences
from pip._internal.models.target_python import TargetPython
from pip._internal.models.wheel import Wheel
from pip._internal.utils.filetypes import WHEEL_EXTENSION
from pip._internal.utils.logging import indent_log
from pip._internal.utils.misc import build_netloc
from pip._internal.utils.packaging import check_requires_python
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.utils.unpacking import SUPPORTED_EXTENSIONS
from pip._internal.utils.urls import url_to_path
from typing import FrozenSet, Iterable, List, Optional, Set, Text, Tuple, Union
from pip._vendor.packaging.tags import Tag
from pip._vendor.packaging.version import _BaseVersion
from pip._internal.index.collector import LinkCollector
from pip._internal.models.search_scope import SearchScope
from pip._internal.req import InstallRequirement
from pip._internal.utils.hashes import Hashes


def find_all_candidates(self, project_name):
    'Find all available InstallationCandidate for project_name\n\n        This checks index_urls and find_links.\n        All versions found are returned as an InstallationCandidate list.\n\n        See LinkEvaluator.evaluate_link() for details on which files\n        are accepted.\n        '
    collected_links = self._link_collector.collect_links(project_name)
    link_evaluator = self.make_link_evaluator(project_name)
    find_links_versions = self.evaluate_links(link_evaluator, links=collected_links.find_links)
    page_versions = []
    for project_url in collected_links.project_urls:
        package_links = self.process_project_url(project_url, link_evaluator=link_evaluator)
        page_versions.extend(package_links)
    file_versions = self.evaluate_links(link_evaluator, links=collected_links.files)
    if file_versions:
        file_versions.sort(reverse=True)
        logger.debug('Local files found: %s', ', '.join([url_to_path(candidate.link.url) for candidate in file_versions]))
    return ((file_versions + find_links_versions) + page_versions)
