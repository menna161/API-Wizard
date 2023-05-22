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


def find_best_candidate(self, project_name, specifier=None, hashes=None):
    'Find matches for the given project and specifier.\n\n        :param specifier: An optional object implementing `filter`\n            (e.g. `packaging.specifiers.SpecifierSet`) to filter applicable\n            versions.\n\n        :return: A `BestCandidateResult` instance.\n        '
    candidates = self.find_all_candidates(project_name)
    candidate_evaluator = self.make_candidate_evaluator(project_name=project_name, specifier=specifier, hashes=hashes)
    return candidate_evaluator.compute_best_candidate(candidates)
