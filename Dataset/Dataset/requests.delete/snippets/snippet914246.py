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


def _delete(url: str) -> requests.Response:
    'Make DELETE request and handle errors.'
    LOG.debug('DELETE %s', url)
    try:
        rsp = requests.delete(url, auth=_get_auth(), headers=_get_headers())
        rsp.raise_for_status()
    except requests.exceptions.RequestException as exc:
        _handle_error('delete', exc)
    LOG.debug('Got response')
    return rsp
