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


def token(self) -> str:
    now = datetime.datetime.now().timestamp()
    if ((now > ((self.since + self.duration) - 60)) or (self._token is None)):
        self.regen_token()
    assert (self._token is not None)
    return self._token
