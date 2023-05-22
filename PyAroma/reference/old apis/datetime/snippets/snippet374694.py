import argparse
import datetime
import os
import re
import sys
import xml.etree.ElementTree as ET


def apply_values_to_nessus(contents, values):
    start = datetime.datetime.now()
    end = (datetime.datetime.now() + datetime.timedelta(0, 1))
    try:
        tree = ET.fromstring(contents)
        name = None
        prefs = tree.findall('Policy/Preferences/PluginsPreferences/item')
        for pref in prefs:
            pref_name = pref.find('preferenceName').text
            pref_selected = pref.find('selectedValue').text
            if (('Offline config file' in pref_name) and pref_selected):
                name = pref_selected
        if (not name):
            raise Exception('Unable to find the config name.')
        for host in values:
            display('Apply values: {}'.format(host), verbose=True)
            preferences = tree.find('Policy/Preferences/ServerPreferences')
            for preference in preferences.findall('preference'):
                if (preference.find('name').text == 'TARGET'):
                    old = preference.find('value').text
                    preference.find('value').text = host
                    break
            report_hosts = tree.findall('Report/ReportHost')
            for report_host in report_hosts:
                report_name = report_host.attrib['name']
                display('Analyzing report: {}'.format(report_name), verbose=True)
                if (report_name.lower() == name.lower()):
                    display('Found report name: {}'.format(name), verbose=True)
                    report_host.attrib['name'] = host
                    old_props = report_host.find('HostProperties')
                    for tag in old_props.findall('tag'):
                        old_props.remove(tag)
                    new_props = values[host]
                    for tag in new_props.findall('tag'):
                        if (tag.attrib['name'] == 'HOST_START_TIMESTAMP'):
                            tag.text = str(unixtime(start))
                        elif (tag.attrib['name'] == 'HOST_END_TIMESTAMP'):
                            tag.text = str(unixtime(end))
                        elif (tag.attrib['name'] == 'HOST_START'):
                            tag.text = start.strftime('%c')
                        elif (tag.attrib['name'] == 'HOST_END'):
                            tag.text = end.strftime('%c')
                        old_props.append(tag)
    except Exception as e:
        display('ERROR: apply_values_to_nessus(): {}'.format(e), exit=1)
        sys.exit(1)
    new_content = ET.tostring(tree, encoding='ascii', method='xml', short_empty_elements=False)
    nessus_content = sanitize_xml_to_nessus(new_content)
    return nessus_content
