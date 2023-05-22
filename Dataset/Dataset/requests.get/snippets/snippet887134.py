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


def show_unread_news():
    '\n    Shows unread news from archlinux.org\n    '
    try:
        os.makedirs(Package.cache_dir, mode=448, exist_ok=True)
    except OSError:
        logging.error('Creating cache dir {} failed'.format(Package.cache_dir))
        raise InvalidInput('Creating cache dir {} failed'.format(Package.cache_dir))
    seen_ids_file = os.path.join(Package.cache_dir, 'seen_news_ids')
    if (not os.path.isfile(seen_ids_file)):
        open(seen_ids_file, 'a').close()
    with open(seen_ids_file, 'r') as seenidsfile:
        seen_ids: Set[str] = set([line for line in seenidsfile.read().strip().splitlines()])
    try:
        news_as_string: str = requests.get('https://www.archlinux.org/feeds/news/', timeout=AurVars.aur_timeout).text
    except requests.exceptions.RequestException:
        logging.error('Connection problem while requesting archlinux.org feed', exc_info=True)
        raise ConnectionProblem('Connection problem while requesting archlinux.org feed')
    news_to_show = list(reversed(list(filter((lambda entry: (entry['id'] not in seen_ids)), feedparser.parse(news_as_string).entries))))
    if (not news_to_show):
        return
    for entry in news_to_show:
        aurman_note('{} [{}]'.format(Colors.BOLD(Colors.LIGHT_MAGENTA(entry['title'])), entry['published']))
        print((re.sub('<[^<]+?>', '', entry['summary']) + '\n'))
    if ask_user('Have you read the {} unread article(s) from archlinux.org?'.format(Colors.BOLD(Colors.LIGHT_MAGENTA(len(news_to_show)))), False):
        with open(seen_ids_file, 'a') as seenidsfile:
            seenidsfile.write(('\n'.join([entry['id'] for entry in news_to_show]) + '\n'))
    else:
        logging.error('User did not read the unseen news, but wanted to install packages on the system')
        raise InvalidInput('User did not read the unseen news, but wanted to install packages on the system')
