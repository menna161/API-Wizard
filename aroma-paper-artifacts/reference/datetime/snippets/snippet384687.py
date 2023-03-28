import logging
import os
import random
import sys
from datetime import datetime
import aws_ir
from aws_ir.libs import aws
from aws_ir.libs import connection
from aws_ir.libs import inventory
from aws_ir.libs import s3bucket


def _generate_case_number(self):
    return datetime.utcnow().strftime('cr-%y-%m%d%H-{0:04x}').format(random.randint(0, (2 ** 16)))
