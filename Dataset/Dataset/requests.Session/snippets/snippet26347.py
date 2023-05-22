import hashlib
import time
import argparse
import requests
import prometheus_client
import lxml.etree
import xml.etree.ElementTree as ET


def scrap_msa(metrics_store, host, login, password):
    session = requests.Session()
    session.verify = False
    creds = hashlib.md5((b'%s_%s' % (login.encode('utf8'), password.encode('utf8')))).hexdigest()
    response = session.get(('https://%s/api/login/%s' % (host, creds)))
    response.raise_for_status()
    session_key = ET.fromstring(response.content)[0][2].text
    session.headers['sessionKey'] = session_key
    session.cookies['wbisessionkey'] = session_key
    session.cookies['wbiusername'] = login
    path_cache = {}
    for (name, metric) in METRICS.items():
        name = (PREFIX + name)
        if isinstance(metric['sources'], dict):
            sources = [metric['sources']]
        else:
            sources = metric['sources']
        for source in sources:
            if (source['path'] not in path_cache):
                response = session.get(('https://%s/api/show/%s' % (host, source['path'])))
                response.raise_for_status()
                path_cache[source['path']] = lxml.etree.fromstring(response.content)
            xml = path_cache[source['path']]
            for obj in xml.xpath(source['object_selector']):
                labels = {source['properties_as_label'][elem.get('name')]: elem.text for elem in obj if (elem.get('name') in source.get('properties_as_label', {}))}
                labels.update(source.get('labels', {}))
                value = obj.find(source['property_selector']).text
                if (value == 'N/A'):
                    value = 'nan'
                metrics_store.get_or_create(metric.get('type', 'gauge'), name, metric['description'], labels).set(value)
