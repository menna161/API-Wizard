import argparse
import base64
import datetime
import os
import re
import sys


def output_audit(items, output):
    content = '<check_type:"Windows" version:"2">\n<group_policy:"Auto-gened: {}">\n\n{}\n\n</group_policy>\n</check_type>'
    now = datetime.datetime.now()
    audit = content.format(now, '\n\n'.join(items).strip())
    with open(output, 'w') as s_out:
        s_out.write((audit.strip() + '\n'))
