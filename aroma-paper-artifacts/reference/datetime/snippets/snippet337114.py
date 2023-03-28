import uuid
from datetime import datetime, date, time as dtime
import time
from passlib.hash import pbkdf2_sha256
from appkernel.model import Marshaller


def from_wire_format(self, wire_value: datetime):
    if isinstance(wire_value, datetime):
        return wire_value.date()
    else:
        return wire_value
