from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, date
import os
import utils
import json
from collections import defaultdict
import re
import urllib.request
import atexit
import copy
import pprint


def write_data_for_website(cve, data):
    'Process data and write out to a JSON file suitable for loading into androidvulnerabilities.org'
    export = dict()
    ref_out = dict()
    for (key, value) in data['References'].items():
        if (key != '*'):
            ref_out[key] = value
    nist_ref = ('NIST-' + cve)
    ref_out[nist_ref] = make_reference(NIST_URL)
    bulletin_ref = ('Bulletin-' + cve)
    ref_out[bulletin_ref] = make_reference(data['URL'])
    discovery_ref = ('Discovery-' + cve)
    ref_out[discovery_ref] = make_reference(data['Discovered_by_ref'])
    discovery_date = None
    if ('Date reported' in data):
        try:
            discovery_date = datetime.strptime(data['Date reported'], '%b %d, %Y').date().isoformat()
        except ValueError:
            pass
    report_date = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}(?=\\.html)', data['URL'])
    export['name'] = cve
    export['CVE'] = [[cve, bulletin_ref]]
    export['Coordinated_disclosure'] = 'unknown'
    export['Categories'] = [data['Category']]
    export['Details'] = check_blank(data['Description'], nist_ref)
    export['Discovered_on'] = check_blank(discovery_date, bulletin_ref)
    export['Discovered_by'] = check_blank(data['Discovered_by'], discovery_ref)
    export['Submission'] = data['Submission']
    if (report_date != None):
        export['Reported_on'] = [[report_date.group(), bulletin_ref]]
    else:
        export['Reported_on'] = []
    export['Fixed_on'] = check_blank(data['Fixed_on'], data['Fixed_on_ref'])
    export['Fix_released_on'] = check_blank(data['Fix_released_on'], bulletin_ref)
    export['Affected_versions'] = check_blank(data['Affected versions'], bulletin_ref)
    export['Affected_devices'] = []
    if ('Affected_versions_regexp' in data):
        export['Affected_versions_regexp'] = [data['Affected_versions_regexp']]
    else:
        export['Affected_versions_regexp'] = [regexp_versions(data['Affected versions'])]
    manufacturer_affected = 'all'
    for manufacturer in KNOWN_MANUFACTURERS:
        if (manufacturer in data['Category']):
            manufacturer_affected = manufacturer
    export['Affected_manufacturers'] = [[manufacturer_affected, bulletin_ref]]
    export['Fixed_versions'] = check_blank(data['Updated AOSP versions'], bulletin_ref)
    if ('Fixed_versions_regexp' in data):
        export['Fixed_versions_regexp'] = [data['Fixed_versions_regexp']]
    else:
        export['Fixed_versions_regexp'] = [regexp_versions(data['Updated AOSP versions'])]
    export['references'] = ref_out
    export['Surface'] = data['Surface']
    export['Vector'] = data['Vector']
    export['Target'] = data['Target']
    export['Channel'] = data['Channel']
    export['Condition'] = data['Condition']
    export['Privilege'] = data['Privilege']
    export['CWE'] = check_blank(data['CWE'], nist_ref)
    with open('website-data/{cve}.json'.format(cve=cve), 'w') as f:
        json.dump(export, f, indent=2)
