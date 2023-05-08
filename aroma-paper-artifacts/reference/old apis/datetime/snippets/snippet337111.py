import uuid
from datetime import datetime, date, time as dtime
import time
from passlib.hash import pbkdf2_sha256
from appkernel.model import Marshaller


def to_wireformat(self, instance_value):
    if isinstance(instance_value, (date, datetime)):
        return time.mktime(instance_value.timetuple())
    else:
        return instance_value
