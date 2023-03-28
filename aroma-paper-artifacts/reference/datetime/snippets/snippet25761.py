from alchemyjsonschema.dictify import dictify
from alchemyjsonschema.tests.models import Group, User
from datetime import datetime
from alchemyjsonschema.tests.models import Group, User
from datetime import datetime
from alchemyjsonschema.tests.models import Group, User
from datetime import datetime


def test_it3():
    from alchemyjsonschema.tests.models import Group, User
    from datetime import datetime
    created_at = datetime(2000, 1, 1)
    group = Group(name='ravenclaw', color='blue', created_at=created_at)
    user = User(name='foo', created_at=created_at, group=group)
    schema = {'type': 'object', 'title': 'User', 'properties': {'pk': {'type': 'integer', 'description': 'primary key'}, 'name': {'type': 'string', 'maxLength': 255}, 'created_at': {'type': 'string', 'format': 'date-time'}, 'group': {'type': 'object', '$ref': '#/definitions/Group'}}, 'required': ['pk', 'name'], 'definitions': {'Group': {'properties': {'pk': {'type': 'integer', 'description': 'primary key'}, 'name': {'type': 'string', 'maxLength': 255}, 'color': {'type': 'string', 'maxLength': 6, 'enum': ['red', 'green', 'yellow', 'blue']}, 'created_at': {'type': 'string', 'format': 'date-time'}}}}}
    result = _callFUT(user, schema)
    assert (result == {'pk': None, 'name': 'foo', 'created_at': created_at, 'group': {'pk': None, 'color': 'blue', 'name': 'ravenclaw', 'created_at': created_at}})
