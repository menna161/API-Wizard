from alchemyjsonschema.dictify import objectify
from alchemyjsonschema import SchemaFactory, ForeignKeyWalker
from alchemyjsonschema.dictify import ModelLookup
import alchemyjsonschema.tests.models as models
from datetime import datetime
from alchemyjsonschema import SchemaFactory, ForeignKeyWalker, InvalidStatus
from alchemyjsonschema.dictify import ModelLookup
import alchemyjsonschema.tests.models as models
from datetime import datetime
import pytest
from alchemyjsonschema import SchemaFactory, ForeignKeyWalker
from alchemyjsonschema.dictify import ModelLookup
import alchemyjsonschema.tests.models as models
from datetime import datetime
from alchemyjsonschema import SchemaFactory, StructuralWalker, RelationDesicion
from alchemyjsonschema.dictify import ModelLookup
import alchemyjsonschema.tests.models as models
from datetime import datetime
from alchemyjsonschema import SchemaFactory, StructuralWalker, UseForeignKeyIfPossibleDecision
from alchemyjsonschema.dictify import ModelLookup
import alchemyjsonschema.tests.models as models
from datetime import datetime
from alchemyjsonschema import SchemaFactory, StructuralWalker
from alchemyjsonschema.dictify import ModelLookup
import alchemyjsonschema.tests.models as models
from datetime import datetime
from alchemyjsonschema import SchemaFactory, StructuralWalker
from alchemyjsonschema.dictify import ModelLookup
import alchemyjsonschema.tests.models as models
from datetime import datetime
from alchemyjsonschema import SchemaFactory, StructuralWalker
from alchemyjsonschema.dictify import ModelLookup
import alchemyjsonschema.tests.models as models
from datetime import datetime
from alchemyjsonschema import SchemaFactory, StructuralWalker
from alchemyjsonschema.dictify import ModelLookup
import alchemyjsonschema.tests.models as models
from datetime import datetime
from alchemyjsonschema import SchemaFactory, StructuralWalker
from alchemyjsonschema.dictify import ModelLookup
import alchemyjsonschema.tests.models as models
from datetime import datetime
from alchemyjsonschema.tests import models
from alchemyjsonschema import SchemaFactory, StructuralWalker
from alchemyjsonschema.dictify import ModelLookup


def test_it_complex2():
    from alchemyjsonschema import SchemaFactory, StructuralWalker
    from alchemyjsonschema.dictify import ModelLookup
    import alchemyjsonschema.tests.models as models
    from datetime import datetime
    factory = SchemaFactory(StructuralWalker)
    group_schema = factory(models.Group)
    created_at = datetime(2000, 1, 1)
    created_at2 = datetime(2001, 1, 1)
    user_dict = dict(name='foo', created_at=created_at)
    group_dict = dict(name='ravenclaw', color='blue', created_at=created_at2, users=[user_dict])
    modellookup = ModelLookup(models)
    result = _callFUT(group_dict, group_schema, modellookup, strict=False)
    assert isinstance(result, models.Group)
    assert (result.pk is None)
    assert (result.name == 'ravenclaw')
    assert (result.color == 'blue')
    assert (result.created_at == datetime(2001, 1, 1))
    assert isinstance(result.users[0], models.User)
    assert (result.users[0].name == 'foo')
    assert (result.users[0].created_at == created_at)
    assert (modellookup.name_stack == [])
