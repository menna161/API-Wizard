import fnmatch
import json
import logging
import os
import re
import sys
from copy import deepcopy
from datetime import datetime
from subprocess import run, DEVNULL
from sys import argv, stdout
from typing import List, Tuple, Dict, Set
import feedparser
import requests
from dateutil.tz import tzlocal
from pycman.config import PacmanConfig
from aurman.aur_utilities import get_aur_info, AurVars
from aurman.bash_completion import possible_completions
from aurman.classes import System, Package, PossibleTypes
from aurman.coloring import aurman_error, aurman_status, aurman_note, Colors
from aurman.help_printing import aurman_help
from aurman.own_exceptions import InvalidInput, ConnectionProblem
from aurman.parse_args import PacmanOperations, parse_pacman_args, PacmanArgs
from aurman.parsing_config import read_config, packages_from_other_sources, AurmanConfig
from aurman.utilities import acquire_sudo, version_comparison, search_and_print, ask_user, strip_versioning_from_name, SudoLoop, SearchSortBy
from aurman.wrappers import pacman, expac
from locale import setlocale, LC_ALL


def show_packages_info(pacman_args: 'PacmanArgs', packages_of_user_names: List[str]) -> None:
    '\n    shows the information of packages, just as pacman -Si\n    :param pacman_args:             the parsed args\n    :param packages_of_user_names:  the targets to show the information of\n    '
    run((['pacman'] + pacman_args.args_as_list()), stderr=DEVNULL)
    for package_dict in get_aur_info(packages_of_user_names):
        for (key, value) in package_dict.items():
            if (type(value) is list):
                value = '  '.join(value)
            elif ((key in ['OutOfDate', 'FirstSubmitted', 'LastModified']) and (value is not None)):
                value = datetime.fromtimestamp(value).replace(tzinfo=tzlocal()).strftime('%c')
            print('{}{} {}'.format(Colors.BOLD(key.ljust(16)), Colors.BOLD(':'), value))
        print()
    sys.exit(0)
