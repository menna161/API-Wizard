import time
import logging
import requests
from rasa.nlu.extractors.duckling_http_extractor import DucklingHTTPExtractor, convert_duckling_format_to_rasa
from rasa.utils.common import raise_warning
from rasa.nlu.training_data import Message
from typing import Any, List, Optional, Text, Dict
from rasa.constants import DOCS_URL_COMPONENTS
from rasa.nlu.constants import ENTITIES


def _duckling_parse(self, text: Text, reference_time: int, timezone) -> List[Dict[(Text, Any)]]:
    'Sends the request to the duckling server and parses the result.'
    try:
        payload = self._payload(text, reference_time)
        payload['tz'] = timezone
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        response = requests.post((self._url() + '/parse'), data=payload, headers=headers, timeout=self.component_config.get('timeout'))
        if (response.status_code == 200):
            return response.json()
        else:
            logger.error('Failed to get a proper response from remote duckling. Status Code: {}. Response: {}'.format(response.status_code, response.text))
            return []
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        logger.error('Failed to connect to duckling http server. Make sure the duckling server is running/healthy/not stale and the proper host and port are set in the configuration. More information on how to run the server can be found on github: https://github.com/facebook/duckling#quickstart Error: {}'.format(e))
        return []
