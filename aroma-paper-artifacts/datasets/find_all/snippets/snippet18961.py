from __future__ import absolute_import
import json
import logging
from pip._vendor import six
from pip._internal.cli import cmdoptions
from pip._internal.cli.req_command import IndexGroupCommand
from pip._internal.exceptions import CommandError
from pip._internal.index.package_finder import PackageFinder
from pip._internal.models.selection_prefs import SelectionPreferences
from pip._internal.self_outdated_check import make_link_collector
from pip._internal.utils.misc import dist_is_editable, get_installed_distributions, tabulate, write_output
from pip._internal.utils.packaging import get_installer


def latest_info(dist):
    typ = 'unknown'
    all_candidates = finder.find_all_candidates(dist.key)
    if (not options.pre):
        all_candidates = [candidate for candidate in all_candidates if (not candidate.version.is_prerelease)]
    evaluator = finder.make_candidate_evaluator(project_name=dist.project_name)
    best_candidate = evaluator.sort_best_candidate(all_candidates)
    if (best_candidate is None):
        return None
    remote_version = best_candidate.version
    if best_candidate.link.is_wheel:
        typ = 'wheel'
    else:
        typ = 'sdist'
    dist.latest_version = remote_version
    dist.latest_filetype = typ
    return dist
