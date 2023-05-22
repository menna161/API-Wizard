from json.decoder import JSONDecodeError
import requests
from requests.exceptions import RequestException
from .owletproperty import OwletProperty
from .owletexceptions import OwletTemporaryCommunicationException
from .owletexceptions import OwletNotInitializedException


def download_logged_data(self):
    'Download "LOGGED_DATA_CACHE", content currently unknown.'
    if (not self.properties):
        raise OwletNotInitializedException('Initialize first - no properties')
    if ('LOGGED_DATA_CACHE' not in self.properties):
        raise OwletNotInitializedException('Initialize first - missing property')
    download_url = self.properties['LOGGED_DATA_CACHE'].value
    download_header = self.owlet_api.get_request_headers()
    try:
        result = requests.get(download_url, headers=download_header, timeout=5)
    except RequestException:
        raise OwletTemporaryCommunicationException('Server Request failed - no answer')
    if (result.status_code != 200):
        raise OwletTemporaryCommunicationException('Server Request failed - return code')
    try:
        json = result.json()
    except JSONDecodeError:
        raise OwletTemporaryCommunicationException('Request failed - JSON invalid')
    if (('datapoint' not in json) or ('file' not in json['datapoint'])):
        raise OwletTemporaryCommunicationException('Request failed - JSON incomplete')
    download_file_url = json['datapoint']['file']
    try:
        result = requests.get(download_file_url)
    except RequestException:
        raise OwletTemporaryCommunicationException('Download Request failed - no answer')
    if (result.status_code != 200):
        raise OwletTemporaryCommunicationException('Download Request failed - status code')
    return result.text
