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


def _deletable_directory(request, onefs_client):
    path = ('/' + new_name(request))
    mode = random.randint(0, MAX_MODE)
    mode &= 511
    onefs_client.mkdir(path=path, mode=mode)
    return (path, {'group': onefs_client.primary_group_of_user(onefs_client.username), 'mode': mode, 'owner': onefs_client.username})
