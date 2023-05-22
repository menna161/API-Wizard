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


def test_it__simple():
    from alchemyjsonschema import SchemaFactory, ForeignKeyWalker
    from alchemyjsonschema.dictify import ModelLookup
    import alchemyjsonschema.tests.models as models
    from datetime import datetime
    factory = SchemaFactory(ForeignKeyWalker)
    user_schema = factory(models.User)
    created_at = datetime(2000, 1, 1)
    user_dict = dict(pk=1, name='foo', created_at=created_at, group_id=10)
    modellookup = ModelLookup(models)
    result = _callFUT(user_dict, user_schema, modellookup)
    assert isinstance(result, models.User)
    assert (result.pk == 1)
    assert (result.name == 'foo')
    assert (result.created_at == datetime(2000, 1, 1))
    assert (result.group_id == 10)
