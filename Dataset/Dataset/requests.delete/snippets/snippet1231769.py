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


@pytest.fixture
def requests_delete_raises():

    class _DummyResponse(object):

        def raise_for_status(self):
            raise requests.exceptions.HTTPError
    with patch('requests.delete', (lambda *args, **kwargs: _DummyResponse())):
        (yield)
