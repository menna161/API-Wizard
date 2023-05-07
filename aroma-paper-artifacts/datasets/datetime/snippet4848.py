import datetime
import json
import pipes
import re
import shlex
import subprocess
from typing import Any, Dict, Optional, cast
import jwt
import requests
from .scopes import Permission
import keen


def __init__(self, integration_id: int, rsadata: Optional[str], personal_account_token: Optional[str], personal_account_name: Optional[str]):
    self.since = int(datetime.datetime.now().timestamp())
    self.duration = (60 * 10)
    self._token = None
    self.integration_id = integration_id
    self.rsadata = rsadata
    self.personal_account_token = personal_account_token
    self.personal_account_name = personal_account_name
    self.idmap: Dict[(str, str)] = {}
    self._org_idmap: Dict[(str, str)] = {}
    self._session_class = Session
