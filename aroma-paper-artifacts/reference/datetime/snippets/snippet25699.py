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


def test_it__jsondict_from_model():
    from alchemyjsonschema import StructuralWalker, SchemaFactory
    from .models import Group, User
    schema_factory = SchemaFactory(StructuralWalker)
    target = _makeOne(schema_factory, Group)
    group = Group(name='ravenclaw', color='blue', created_at=_datetime(2000, 1, 1, 10, 0, 0, 0))
    group.users = [User(name='foo', created_at=_datetime(2000, 1, 1, 10, 0, 0, 0))]
    jsondict = target.jsondict_from_object(group, verbose=True)
    import json
    assert json.dumps(jsondict)
    assert (jsondict == {'color': 'blue', 'name': 'ravenclaw', 'users': [{'name': 'foo', 'pk': None, 'created_at': '2000-01-01T10:00:00+00:00'}], 'pk': None, 'created_at': '2000-01-01T10:00:00+00:00'})
