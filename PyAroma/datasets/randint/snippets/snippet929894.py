import functools
import os
import pathlib
import random
import unittest
import uuid
from typing import Any
from typing import Callable
from typing import Type
from typing import TypeVar
from typing import cast
import pytest
from django.conf import settings as django_settings
from django.utils.module_loading import import_string
from typing_extensions import Final
from collectfast import settings


def create_static_file() -> pathlib.Path:
    'Write random characters to a file in the static directory.'
    path = (static_dir / f'{uuid.uuid4().hex}.txt')
    path.write_text(''.join((chr(random.randint(0, 64)) for _ in range(500))))
    return path
