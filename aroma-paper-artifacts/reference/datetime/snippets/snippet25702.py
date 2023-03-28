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


def test_it__object_from_dict():
    from alchemyjsonschema import StructuralWalker, SchemaFactory
    from .models import Group, User
    schema_factory = SchemaFactory(StructuralWalker)
    target = _makeOne(schema_factory, Group)
    group_dict = {'color': 'blue', 'users': [{'created_at': _datetime(2000, 1, 1, 10, 0, 0, 0), 'pk': None, 'name': 'foo'}], 'created_at': _datetime(2000, 1, 1, 10, 0, 0, 0), 'pk': None, 'name': 'ravenclaw'}
    group = target.object_from_dict(group_dict, strict=False)
    assert isinstance(group, Group)
    assert (group.color == 'blue')
    assert (group.name == 'ravenclaw')
    assert (group.pk is None)
    assert (group.created_at == _datetime(2000, 1, 1, 10, 0, 0, 0))
    assert ((len(group.users) == 1) and isinstance(group.users[0], User))
    assert (group.users[0].name == 'foo')
    assert (group.users[0].pk is None)
    assert (group.users[0].created_at == _datetime(2000, 1, 1, 10, 0, 0, 0))
