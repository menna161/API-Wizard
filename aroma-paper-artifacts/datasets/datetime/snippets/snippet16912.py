from __future__ import absolute_import
import datetime
import hashlib
import json
import logging
import os.path
import sys
from pip._vendor import pkg_resources
from pip._vendor.packaging import version as packaging_version
from pip._vendor.six import ensure_binary
from pip._internal.index.collector import LinkCollector
from pip._internal.index.package_finder import PackageFinder
from pip._internal.models.search_scope import SearchScope
from pip._internal.models.selection_prefs import SelectionPreferences
from pip._internal.utils.filesystem import adjacent_tmp_file, check_path_owner, replace
from pip._internal.utils.misc import ensure_dir, get_installed_version, redact_auth_from_url
from pip._internal.utils.packaging import get_installer
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
import optparse
from optparse import Values
from typing import Any, Dict, Text, Union
from pip._internal.network.session import PipSession


def pip_self_version_check(session, options):
    "Check for an update for pip.\n\n    Limit the frequency of checks to once per week. State is stored either in\n    the active virtualenv or in the user's USER_CACHE_DIR keyed off the prefix\n    of the pip script path.\n    "
    installed_version = get_installed_version('pip')
    if (not installed_version):
        return
    pip_version = packaging_version.parse(installed_version)
    pypi_version = None
    try:
        state = SelfCheckState(cache_dir=options.cache_dir)
        current_time = datetime.datetime.utcnow()
        if (('last_check' in state.state) and ('pypi_version' in state.state)):
            last_check = datetime.datetime.strptime(state.state['last_check'], SELFCHECK_DATE_FMT)
            if ((current_time - last_check).total_seconds() < (((7 * 24) * 60) * 60)):
                pypi_version = state.state['pypi_version']
        if (pypi_version is None):
            link_collector = make_link_collector(session, options=options, suppress_no_index=True)
            selection_prefs = SelectionPreferences(allow_yanked=False, allow_all_prereleases=False)
            finder = PackageFinder.create(link_collector=link_collector, selection_prefs=selection_prefs)
            best_candidate = finder.find_best_candidate('pip').best_candidate
            if (best_candidate is None):
                return
            pypi_version = str(best_candidate.version)
            state.save(pypi_version, current_time)
        remote_version = packaging_version.parse(pypi_version)
        local_version_is_older = ((pip_version < remote_version) and (pip_version.base_version != remote_version.base_version) and was_installed_by_pip('pip'))
        if (not local_version_is_older):
            return
        pip_cmd = '{} -m pip'.format(sys.executable)
        logger.warning("You are using pip version %s; however, version %s is available.\nYou should consider upgrading via the '%s install --upgrade pip' command.", pip_version, pypi_version, pip_cmd)
    except Exception:
        logger.debug('There was an error checking the latest version of pip', exc_info=True)
