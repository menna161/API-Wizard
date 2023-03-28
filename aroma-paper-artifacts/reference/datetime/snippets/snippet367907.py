import enum
from uuid import uuid4, UUID
from datetime import date, datetime, timedelta
from asyncpgsa import connection
from sqlalchemy import Table, Column, MetaData, Sequence, types
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


def test_update_query():
    query = users.update().where((users.c.name == 'default'))
    query = query.values(name='newname', serial=5555, t_list=['l3', 'l4'], t_enum=MyEnum.ITEM_1, t_int_enum=MyIntEnum.ITEM_2, t_datetime=datetime(2030, 1, 1), t_date=date(2030, 1, 1), t_date_2=date(2030, 1, 1), t_interval=timedelta(seconds=180), t_boolean=False)
    (new_query, new_params) = connection.compile_query(query)
    assert query.parameters.get('version')
    assert (query.parameters.get('serial') == 5555)
    assert (query.parameters.get('name') == 'newname')
    assert (query.parameters.get('t_list') == ['l3', 'l4'])
    assert (query.parameters.get('t_enum') == MyEnum.ITEM_1)
    assert (query.parameters.get('t_int_enum') == MyIntEnum.ITEM_2)
    assert (query.parameters.get('t_datetime') == datetime(2030, 1, 1))
    assert (query.parameters.get('t_date') == date(2030, 1, 1))
    assert (query.parameters.get('t_date_2') == date(2030, 1, 1))
    assert (query.parameters.get('t_interval') == timedelta(seconds=180))
    assert (query.parameters.get('t_boolean') == False)
    assert isinstance(query.parameters.get('version'), UUID)
