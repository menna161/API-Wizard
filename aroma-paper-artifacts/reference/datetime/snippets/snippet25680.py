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


def test_it__dictify2():
    from alchemyjsonschema import SchemaFactory, StructuralWalker
    from alchemyjsonschema.tests.models import Group, User
    from datetime import datetime
    factory = SchemaFactory(StructuralWalker)
    user_schema = factory(User)
    created_at = datetime(2000, 1, 1)
    group = Group(name='ravenclaw', color='blue', created_at=created_at)
    user = User(name='foo', created_at=created_at, group=group)
    result = _callFUT(user, user_schema)
    assert (result == {'pk': None, 'name': 'foo', 'created_at': created_at, 'group': {'pk': None, 'color': 'blue', 'name': 'ravenclaw', 'created_at': created_at}})
