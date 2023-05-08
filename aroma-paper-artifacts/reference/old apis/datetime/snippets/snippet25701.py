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


def test_it__dict_from_jsondict():
    from alchemyjsonschema import StructuralWalker, SchemaFactory
    from .models import Group
    schema_factory = SchemaFactory(StructuralWalker)
    target = _makeOne(schema_factory, Group)
    jsondict = {'color': 'blue', 'name': 'ravenclaw', 'users': [{'name': 'foo', 'pk': 10, 'created_at': '2000-01-01T10:00:00+00:00'}], 'pk': None, 'created_at': '2000-01-01T10:00:00+00:00'}
    group_dict = target.dict_from_jsondict(jsondict)
    assert (group_dict == {'color': 'blue', 'users': [{'created_at': _datetime(2000, 1, 1, 10, 0, 0, 0), 'pk': 10, 'name': 'foo'}], 'created_at': _datetime(2000, 1, 1, 10, 0, 0, 0), 'pk': None, 'name': 'ravenclaw'})
