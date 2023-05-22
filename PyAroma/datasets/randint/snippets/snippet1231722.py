import configparser
from contextlib2 import ExitStack as does_not_raise
from enum import Enum
import json
import os
import random
import tempfile
from unittest.mock import Mock, patch
import uuid
import kadmin
import pytest
import requests
import urllib3
from isilon_hadoop_tools import directories, identities, onefs, IsilonHadoopToolError


def new_id():
    'Get an ID that may be used to create a new user or group.'
    return random.randint(1024, 65536)
