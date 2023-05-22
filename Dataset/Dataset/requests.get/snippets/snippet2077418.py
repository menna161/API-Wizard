import os
import re
import logging
import subprocess
import datetime as dt
from time import sleep
import requests
from pyedgar import config
from pyedgar import utilities


def download_form_from_web(cik, accession=None):
    '\n    Sometimes the cache file is not there, or you do not have local cache.\n    In those cases, you can download the EDGAR forms from S3 directly.\n\n    Arguments:\n        cik (str,dict,object): String CIK, or object with cik and accession attributes or keys.\n        accession (str): String ACCESSION number, or None if accession in CIK object.\n\n    Returns:\n        tuple: Tuple of strings in the form (bulk DL url, user website url)\n    '
    (_raw, _) = get_edgar_urls(cik, accession=accession)
    r = requests.get(_raw, headers=REQUEST_HEADERS)
    data = r.content
    for (_decode_type, _errors) in zip(('latin-1', 'utf-8', 'latin-1'), ('strict', 'strict', 'ignore')):
        try:
            return data.decode(_decode_type, errors=_errors)
        except (UnicodeDecodeError, ValueError):
            continue
