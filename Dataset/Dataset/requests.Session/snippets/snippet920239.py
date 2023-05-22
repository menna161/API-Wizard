from __future__ import unicode_literals
import os
import pytest
import requests
import rtpy
from .mixins import RtpyTestMixin


def test_optional_keys_in_settings(self, instantiate_af_objects_credentials_and_api_key):
    'Optional keys in settings tests.'
    my_settings = {'raw_response': True}
    r = self.af.system_and_configuration.system_health_ping(settings=my_settings)
    if (not r.status_code):
        message = 'raw response setting did not apply properly!'
        raise self.RtpyTestError(message)
    my_settings = {'verbose_level': 1}
    r = self.af.system_and_configuration.system_health_ping(settings=my_settings)
    session = requests.Session()
    my_settings = {'session': session}
    r = self.af.system_and_configuration.system_health_ping(settings=my_settings)
