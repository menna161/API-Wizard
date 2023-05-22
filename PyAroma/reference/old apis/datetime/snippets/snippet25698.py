import pytz
from datetime import datetime
from alchemyjsonschema.mapping import Draft4MappingFactory
import alchemyjsonschema.tests.models as models
from alchemyjsonschema import StructuralWalker, SchemaFactory
from .models import Group, User
from alchemyjsonschema import StructuralWalker, SchemaFactory
from .models import Group, User
import json
from alchemyjsonschema import StructuralWalker, SchemaFactory
from .models import Group
from alchemyjsonschema import StructuralWalker, SchemaFactory
from .models import Group
from alchemyjsonschema import StructuralWalker, SchemaFactory
from .models import Group, User


def test_it__dict_from_model_object():
    from alchemyjsonschema import StructuralWalker, SchemaFactory
    from .models import Group, User
    schema_factory = SchemaFactory(StructuralWalker)
    target = _makeOne(schema_factory, Group)
    group = Group(name='ravenclaw', color='blue', created_at=_datetime(2000, 1, 1, 10, 0, 0, 0))
    group.users = [User(name='foo', created_at=_datetime(2000, 1, 1, 10, 0, 0, 0))]
    group_dict = target.dict_from_object(group)
    assert (group_dict == {'color': 'blue', 'users': [{'created_at': _datetime(2000, 1, 1, 10, 0, 0, 0), 'pk': None, 'name': 'foo'}], 'created_at': _datetime(2000, 1, 1, 10, 0, 0, 0), 'pk': None, 'name': 'ravenclaw'})
