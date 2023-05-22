import uuid
from datetime import datetime, date, time as dtime
import time
from passlib.hash import pbkdf2_sha256
from appkernel.model import Marshaller


def from_wire_format(self, wire_value):
    if isinstance(wire_value, str):
        wire_value = float(wire_value)
    if isinstance(wire_value, (float, int)):
        return datetime.fromtimestamp(wire_value)
    else:
        return wire_value
