from contextlib import contextmanager
import datetime
import uuid
import sqlalchemy as sa
from sqlalchemy.inspection import inspect
from a10_neutron_lbaas.db import api as db_api


def _get_date():
    return datetime.datetime.now()
