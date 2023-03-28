from enum import Enum as _Enum
from Acquire.Service import Service as _Service
import random as _random
from Acquire.Service import Service as _Service
from Acquire.Service import Service as _Service
from Acquire.Service import Service as _Service
from Acquire.Client import Authorisation as _Authorisation
from Acquire.Client import create_qrcode as _create_qrcode
from Acquire.Client import Credentials as _Credentials
import re
from Acquire.Client import create_qrcode as _create_qrcode
from Acquire.Client import LoginError
from Acquire.Client import PrivateKey as _PrivateKey
from Acquire.Identity import LoginSession as _LoginSession
from Acquire.ObjectStore import bytes_to_string as _bytes_to_string
import time as _time
from Acquire.Service import Service as _Service
from Acquire.Client import LoginError
from Acquire.Service import Service as _Service
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.Client import Authorisation as _Authorisation
from Acquire.ObjectStore import bytes_to_string as _bytes_to_string
from Acquire.Service import Service as _Service
from Acquire.Client import UserError


def wait_for_login(self, timeout=None, polling_delta=5):
    "Block until the user has logged in. If 'timeout' is set\n           then we will wait for a maximum of that number of seconds\n\n           This will check whether we have logged in by polling\n           the identity service every 'polling_delta' seconds.\n        "
    self._check_for_error()
    if (not self.is_logging_in()):
        return self.is_logged_in()
    polling_delta = int(polling_delta)
    if (polling_delta > 60):
        polling_delta = 60
    elif (polling_delta < 1):
        polling_delta = 1
    import time as _time
    if (timeout is None):
        while True:
            self._poll_session_status()
            if self.is_logged_in():
                return True
            elif (not self.is_logging_in()):
                return False
            _time.sleep(polling_delta)
    else:
        timeout = int(timeout)
        if (timeout < 1):
            timeout = 1
        from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
        start_time = _get_datetime_now()
        while ((_get_datetime_now() - start_time).seconds < timeout):
            self._poll_session_status()
            if self.is_logged_in():
                return True
            elif (not self.is_logging_in()):
                return False
            _time.sleep(polling_delta)
        return False
