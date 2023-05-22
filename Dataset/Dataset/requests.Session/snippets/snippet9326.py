import time
import logging
import re
from typing import Any, Iterator, Optional
import requests
from .auth_config import PCOAuthConfig
from .exceptions import PCORequestTimeoutException, PCORequestException, PCOUnexpectedRequestException


def __init__(self, application_id: Optional[str]=None, secret: Optional[str]=None, token: Optional[str]=None, cc_name: Optional[str]=None, api_base: str='https://api.planningcenteronline.com', timeout: int=60, upload_url: str='https://upload.planningcenteronline.com/v2/files', upload_timeout: int=300, timeout_retries: int=3):
    self._log = logging.getLogger(__name__)
    self._auth_config = PCOAuthConfig(application_id, secret, token, cc_name)
    self._auth_header = self._auth_config.auth_header
    self.api_base = api_base
    self.timeout = timeout
    self.upload_url = upload_url
    self.upload_timeout = upload_timeout
    self.timeout_retries = timeout_retries
    self.session = requests.Session()
    self._log.debug('Pypco has been initialized!')
