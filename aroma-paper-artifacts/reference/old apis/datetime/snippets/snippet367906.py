import enum
from uuid import uuid4, UUID
from datetime import date, datetime, timedelta
from asyncpgsa import connection
from sqlalchemy import Table, Column, MetaData, Sequence, types
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


def test_insert_query_defaults_override():
    query = users.insert()
    query = query.values(name='username', serial=4444, t_list=['l1', 'l2'], t_enum=MyEnum.ITEM_1, t_int_enum=MyIntEnum.ITEM_2, t_datetime=datetime(2020, 1, 1), t_date=date(2020, 1, 1), t_date_2=date(2020, 1, 1), t_interval=timedelta(seconds=120), t_boolean=False)
    (new_query, new_params) = connection.compile_query(query)
    assert query.parameters.get('version')
    assert (query.parameters.get('serial') == 4444)
    assert (query.parameters.get('name') == 'username')
    assert (query.parameters.get('t_list') == ['l1', 'l2'])
    assert (query.parameters.get('t_enum') == MyEnum.ITEM_1)
    assert (query.parameters.get('t_int_enum') == MyIntEnum.ITEM_2)
    assert (query.parameters.get('t_datetime') == datetime(2020, 1, 1))
    assert (query.parameters.get('t_date') == date(2020, 1, 1))
    assert (query.parameters.get('t_date_2') == date(2020, 1, 1))
    assert (query.parameters.get('t_interval') == timedelta(seconds=120))
    assert (query.parameters.get('t_boolean') == False)
    assert isinstance(query.parameters.get('version'), UUID)
