import json
import requests
import xmltodict
from lxml import etree
from .constants import LABEL_ZPL, SERVICE_PRIORITY


def send_request(self, action, xml):
    xml = etree.tostring(xml, encoding='iso-8859-1', pretty_print=self.test).decode()
    url = self.get_url(action, xml)
    xml_response = requests.get(url).content
    response = json.loads(json.dumps(xmltodict.parse(xml_response)))
    if ('Error' in response):
        raise USPSApiError(response['Error']['Description'])
    return response
