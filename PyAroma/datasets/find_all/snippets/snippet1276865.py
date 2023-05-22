import sys
import atexit
from collections.abc import MutableMapping
import contextlib
import distutils.version
import functools
import io
import importlib
import inspect
from inspect import Parameter
import locale
import logging
import os
from pathlib import Path
import pprint
import re
import shutil
import stat
import subprocess
import tempfile
import urllib.request
import warnings
from . import cbook, rcsetup
from matplotlib.cbook import MatplotlibDeprecationWarning, dedent, get_label, sanitize_sequence
from matplotlib.cbook import mplDeprecation
from matplotlib.rcsetup import defaultParams, validate_backend, cycler
import numpy
from ._version import get_versions
import dateutil
import pyparsing
import platform
from matplotlib import ft2font
import matplotlib.afm
from .style.core import STYLE_BLACKLIST
from .style.core import STYLE_BLACKLIST
from .style.core import STYLE_BLACKLIST
import faulthandler
import pytest
import pytest
from matplotlib.pyplot import switch_backend
from matplotlib import pyplot as plt


def find_all(self, pattern):
    '\n        Return the subset of this RcParams dictionary whose keys match,\n        using :func:`re.search`, the given ``pattern``.\n\n        .. note::\n\n            Changes to the returned dictionary are *not* propagated to\n            the parent RcParams dictionary.\n\n        '
    pattern_re = re.compile(pattern)
    return RcParams(((key, value) for (key, value) in self.items() if pattern_re.search(key)))
