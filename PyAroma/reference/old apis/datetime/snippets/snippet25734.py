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


def test_it_complex__partial():
    from alchemyjsonschema import SchemaFactory, StructuralWalker
    from alchemyjsonschema.dictify import ModelLookup
    import alchemyjsonschema.tests.models as models
    from datetime import datetime
    factory = SchemaFactory(StructuralWalker)
    user_schema = factory(models.User)
    created_at = datetime(2000, 1, 1)
    user_dict = dict(name='foo', created_at=created_at)
    modellookup = ModelLookup(models)
    result = _callFUT(user_dict, user_schema, modellookup, strict=False)
    assert isinstance(result, models.User)
    assert (result.pk is None)
    assert (result.name == 'foo')
    assert (result.created_at == datetime(2000, 1, 1))
    assert (result.group_id is None)
    assert (modellookup.name_stack == [])
