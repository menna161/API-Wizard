from __future__ import print_function
import os
import os.path
import re
import time
import sys
import hashlib
import json
import difflib
import tempfile
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.errorhandler import NoSuchElementException
from xml.etree import ElementTree
from colorama import Fore, Back, Style


def pull(table, local_storage, status_file):
    '\n    Update the local files with changes made in Alma.\n\n    This will download letters whose remote checksum does not match the value in status.json.\n\n    Params:\n        table: TemplateConfigurationTable object\n        local_storage: LocalStorage object\n        status_file: StatusFile object\n    '
    today = datetime.now().strftime('%d/%m/%Y')
    count_new = 0
    count_changed = 0
    for (idx, filename) in enumerate(table.filenames):
        progress = ('%3d/%3d' % ((idx + 1), len(table.filenames)))
        table.print_letter_status(filename, '', progress)
        if ((table.modified(filename) == status_file.modified(filename)) and (status_file.modified(filename) != today)):
            table.print_letter_status(filename, 'no changes', progress, True)
            continue
        table.print_letter_status(filename, 'checking...', progress)
        try:
            if table.is_customized(filename):
                content = table.open_letter(filename)
            else:
                content = table.open_default_letter(filename)
        except TimeoutException:
            table.print_letter_status(filename, 'retrying...', progress)
            if table.is_customized(filename):
                content = table.open_letter(filename)
            else:
                content = table.open_default_letter(filename)
        table.close_letter()
        old_sha1 = status_file.checksum(filename)
        if (content.sha1 == old_sha1):
            table.print_letter_status(filename, 'no changes', progress, True)
            continue
        if (not local_storage.store(filename, content, table.modified(filename))):
            table.print_letter_status(filename, ((Fore.RED + 'skipped due to conflict') + Style.RESET_ALL), progress, True)
            continue
        if (old_sha1 is None):
            count_new += 1
            table.print_letter_status(filename, ((Fore.GREEN + 'fetched new letter @ {}'.format(content.sha1[0:7])) + Style.RESET_ALL), progress, True)
        else:
            count_changed += 1
            table.print_letter_status(filename, ((Fore.GREEN + 'updated from {} to {}'.format(old_sha1[0:7], content.sha1[0:7])) + Style.RESET_ALL), progress, True)
    sys.stdout.write(((Fore.GREEN + 'Fetched {} new, {} changed letters\n'.format(count_new, count_changed)) + Style.RESET_ALL))
