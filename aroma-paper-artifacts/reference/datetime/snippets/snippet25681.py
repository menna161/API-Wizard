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


def test_it__normalize():
    from alchemyjsonschema import SchemaFactory, StructuralWalker
    from alchemyjsonschema.tests.models import Group
    from datetime import datetime
    import pytz
    created_at = datetime(2000, 1, 1, 0, 0, 0, 0, pytz.utc)
    factory = SchemaFactory(StructuralWalker)
    group_schema = factory(Group)
    group_dict = {'name': 'ravenclaw', 'created_at': '2000-01-01T00:00:00+00:00', 'color': 'blue', 'pk': None, 'users': [{'name': 'foo', 'created_at': '2000-01-01T00:00:00+00:00', 'pk': None}, {'name': 'boo', 'created_at': '2000-01-01T00:00:00+00:00', 'pk': None}]}
    result = _callFUT2(group_dict, group_schema)
    assert (result == {'pk': None, 'color': 'blue', 'name': 'ravenclaw', 'created_at': created_at, 'users': [{'pk': None, 'name': 'foo', 'created_at': created_at}, {'pk': None, 'name': 'boo', 'created_at': created_at}]})
