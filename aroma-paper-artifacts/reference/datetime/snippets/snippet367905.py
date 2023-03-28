import enum
from uuid import uuid4, UUID
from datetime import date, datetime, timedelta
from asyncpgsa import connection
from sqlalchemy import Table, Column, MetaData, Sequence, types
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


def test_insert_query_defaults():
    query = users.insert()
    (new_query, new_params) = connection.compile_query(query)
    serial_default = query.parameters.get('serial')
    assert (serial_default.name == 'nextval')
    assert (serial_default.clause_expr.element.clauses[0].value == 'serial_seq')
    assert (query.parameters.get('name') == name_default)
    assert (query.parameters.get('t_list') == t_list_default)
    assert (query.parameters.get('t_enum') == t_enum_default)
    assert (query.parameters.get('t_int_enum') == t_int_enum_default)
    assert (query.parameters.get('t_datetime') == t_datetime_default)
    assert (query.parameters.get('t_date') == t_date_default)
    assert (query.parameters.get('t_date_2') == t_date_2_default())
    assert (query.parameters.get('t_interval') == t_interval_default)
    assert isinstance(query.parameters.get('version'), UUID)
    assert (query.parameters.get('t_boolean') == t_boolean_default)
