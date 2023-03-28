import argparse
import datetime
import os
import re
import sys


def output_audit(items, output):
    content = '# {}\n<check_type:"Unix">\n\n{}\n\n</check_type>'
    now = datetime.datetime.now()
    audit = content.format(now, '\n\n'.join(items).strip())
    with open(output, 'w') as s_out:
        s_out.write((audit.strip() + '\n'))
