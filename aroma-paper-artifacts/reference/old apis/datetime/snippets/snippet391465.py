from __future__ import print_function, unicode_literals, division, absolute_import
import logging
import os, sys, json, subprocess, argparse
import platform
import py_compile
import re
import shutil
import tempfile
import time
from datetime import datetime
import dxpy
import dxpy.app_builder
import dxpy.workflow_builder
import dxpy.executable_builder
from .. import logger
from dxpy.nextflow.nextflow_builder import build_pipeline_from_repository, prepare_nextflow
from dxpy.nextflow.nextflow_utils import get_resources_subpath
from ..utils import json_load_raise_on_duplicates
from ..utils.resolver import resolve_path, check_folder_exists, ResolutionError, is_container_id
from ..utils.completer import LocalCompleter
from ..app_categories import APP_CATEGORIES
from ..exceptions import err_exit
from ..utils.printing import BOLD
from ..compat import open, USING_PYTHON2, decode_command_line_args, basestring


def _get_timestamp_version_suffix(version):
    if ('+' in version):
        return ('.build.' + datetime.today().strftime('%Y%m%d.%H%M'))
    else:
        return ('+build.' + datetime.today().strftime('%Y%m%d.%H%M'))
