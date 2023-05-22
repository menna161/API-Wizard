from functools import update_wrapper
import logging
import os.path
import re
import sys
import tempfile
import typing as ty
import click
import requests
import git_pw
from git_pw import config


def _get(url: str, params: ty.Optional[Filters]=None, stream: bool=False) -> requests.Response:
    'Make GET request and handle errors.'
    LOG.debug('GET %s', url)
    try:
        rsp = requests.get(url, auth=_get_auth(optional=True), headers=_get_headers(), stream=stream, params=params)
        rsp.raise_for_status()
    except requests.exceptions.RequestException as exc:
        _handle_error('fetch', exc)
    LOG.debug('Got response')
    return rsp
