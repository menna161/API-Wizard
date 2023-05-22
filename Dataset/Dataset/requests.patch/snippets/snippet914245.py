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


def _patch(url: str, data: ty.List[ty.Tuple[(str, ty.Any)]]) -> requests.Response:
    'Make PATCH request and handle errors.'
    LOG.debug('PATCH %s, data=%r', url, data)
    try:
        rsp = requests.patch(url, auth=_get_auth(), headers=_get_headers(), data=data)
        rsp.raise_for_status()
    except requests.exceptions.RequestException as exc:
        _handle_error('update', exc)
    LOG.debug('Got response')
    return rsp
