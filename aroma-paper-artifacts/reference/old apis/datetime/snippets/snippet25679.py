from alchemyjsonschema.dictify import dictify
from alchemyjsonschema.dictify import normalize
from alchemyjsonschema.dictify import prepare
from alchemyjsonschema.dictify import jsonify
from alchemyjsonschema import SchemaFactory, StructuralWalker
from alchemyjsonschema.tests.models import Group, User
from datetime import datetime
from alchemyjsonschema import SchemaFactory, StructuralWalker
from alchemyjsonschema.tests.models import Group, User
from datetime import datetime
from alchemyjsonschema import SchemaFactory, StructuralWalker
from alchemyjsonschema.tests.models import Group
from datetime import datetime
import pytz
from alchemyjsonschema import SchemaFactory, StructuralWalker
from alchemyjsonschema.tests.models import User
from alchemyjsonschema import SchemaFactory, StructuralWalker
from alchemyjsonschema.tests.models import Group
from alchemyjsonschema import SchemaFactory, StructuralWalker
from alchemyjsonschema.tests.models import User
from alchemyjsonschema import SchemaFactory, StructuralWalker
from alchemyjsonschema.tests.models import Group
from alchemyjsonschema import SchemaFactory, StructuralWalker
from alchemyjsonschema.tests.models import Group
from alchemyjsonschema import SchemaFactory, StructuralWalker
from alchemyjsonschema.tests.models import Group, User
from datetime import datetime


def test_it__dictify():
    from alchemyjsonschema import SchemaFactory, StructuralWalker
    from alchemyjsonschema.tests.models import Group, User
    from datetime import datetime
    factory = SchemaFactory(StructuralWalker)
    group_schema = factory(Group)
    created_at = datetime(2000, 1, 1)
    users = [User(name='foo', created_at=created_at), User(name='boo', created_at=created_at)]
    group = Group(name='ravenclaw', color='blue', users=users, created_at=created_at)
    result = _callFUT(group, group_schema)
    assert (result == {'pk': None, 'color': 'blue', 'name': 'ravenclaw', 'created_at': created_at, 'users': [{'pk': None, 'name': 'foo', 'created_at': created_at}, {'pk': None, 'name': 'boo', 'created_at': created_at}]})
