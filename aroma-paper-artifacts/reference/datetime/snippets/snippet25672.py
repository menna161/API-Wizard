from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from alchemyjsonschema import SchemaFactory
from alchemyjsonschema import ForeignKeyWalker
from alchemyjsonschema import ForeignKeyWalker
from alchemyjsonschema import ForeignKeyWalker
from datetime import datetime
from alchemyjsonschema import ForeignKeyWalker
from alchemyjsonschema import ForeignKeyWalker


def test_detect__nullable_is_False__but_default_is_exists__not_required():
    from alchemyjsonschema import ForeignKeyWalker
    from datetime import datetime

    class Model2(Base):
        __tablename__ = 'Model2'
        pk = sa.Column(sa.Integer, primary_key=True, doc='primary key')
        created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    target = _makeOne(ForeignKeyWalker)
    walker = target.walker(Model2)
    result = target._detect_required(walker)
    assert (result == ['pk'])
