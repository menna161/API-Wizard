from __future__ import absolute_import
import json
import logging
from pip._vendor import six
from pip._vendor.six.moves import zip_longest
from pip._internal.cli import cmdoptions
from pip._internal.cli.base_command import Command
from pip._internal.exceptions import CommandError
from pip._internal.index import PackageFinder
from pip._internal.utils.misc import dist_is_editable, get_installed_distributions
from pip._internal.utils.packaging import get_installer


def iter_packages_latest_infos(self, packages, options):
    index_urls = ([options.index_url] + options.extra_index_urls)
    if options.no_index:
        logger.debug('Ignoring indexes: %s', ','.join(index_urls))
        index_urls = []
    with self._build_session(options) as session:
        finder = self._build_package_finder(options, index_urls, session)
        for dist in packages:
            typ = 'unknown'
            all_candidates = finder.find_all_candidates(dist.key)
            if (not options.pre):
                all_candidates = [candidate for candidate in all_candidates if (not candidate.version.is_prerelease)]
            evaluator = finder.candidate_evaluator
            best_candidate = evaluator.get_best_candidate(all_candidates)
            if (best_candidate is None):
                continue
            remote_version = best_candidate.version
            if best_candidate.location.is_wheel:
                typ = 'wheel'
            else:
                typ = 'sdist'
            dist.latest_version = remote_version
            dist.latest_filetype = typ
            (yield dist)
