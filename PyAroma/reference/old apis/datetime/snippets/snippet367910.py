import pytest
import os
import enum
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, MetaData, types, Sequence
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.engine import create_engine
from . import URL


@pytest.fixture(scope='module')
def test_querying_table(metadata):
    '\n    Create an object for test table.\n\n    '
    worker_id = os.environ.get('PYTEST_XDIST_WORKER', 'master')
    return Table(('test_querying_table_' + worker_id), metadata, Column('id', types.Integer, autoincrement=True, primary_key=True), Column('serial', types.Integer, Sequence('serial_seq')), Column('t_string', types.String(60), onupdate='updated'), Column('t_list', types.ARRAY(types.String(60))), Column('t_enum', types.Enum(MyEnum)), Column('t_int_enum', types.Enum(MyIntEnum)), Column('t_datetime', types.DateTime()), Column('t_date', types.DateTime()), Column('t_interval', types.Interval()), Column('uniq_uuid', PG_UUID, nullable=False, unique=True, default=uuid4))
