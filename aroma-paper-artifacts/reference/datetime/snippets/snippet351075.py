from __future__ import absolute_import, division, print_function
import io
import requests
import urllib3
import os
from datetime import datetime
from ansible.errors import AnsibleParserError
from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible.plugins.lookup import LookupBase


def build_logfile(self, site):
    '\n        Logs which switches were used for configuration\n        :param site: site name for variables\n        '
    skip_list = []
    done_list = []
    for key in self.switch_data:
        if (not self.switch_data[key][2]):
            skip_list.append([key, self.switch_data[key][0], self.switch_data[key][1]])
        else:
            done_list.append([key, self.switch_data[key][0], self.switch_data[key][1]])
    if (not os.path.exists('./ztp_logs/')):
        os.makedirs('./ztp_logs/')
    with io.open((('./ztp_logs/' + site) + '.txt'), 'w') as outfile:
        outfile.write((datetime.now().strftime('%I:%M%p on %B %d, %Y') + '\n').decode('unicode-escape'))
        outfile.write(u'\n *****The following switches got skipped in this run***** \n')
        for switch in skip_list:
            outfile.write(((((((u'MAC:' + str(switch[0]).decode('unicode-escape')) + ', IP: ') + str(switch[1]).decode('unicode-escape')) + ', Hostname: ') + str(switch[2]).decode('unicode-escape')) + '\n'))
        outfile.write(u'\n *****The following switches got configured or are already configured with a static ip**** \n')
        for switch in done_list:
            outfile.write(((((((u'MAC:' + str(switch[0]).decode('unicode-escape')) + ', IP: ') + str(switch[1]).decode('unicode-escape')) + ', Hostname: ') + str(switch[2]).decode('unicode-escape')) + '\n'))
    return skip_list
