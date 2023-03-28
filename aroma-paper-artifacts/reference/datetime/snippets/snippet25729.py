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


def test_it__strict_true__then__required_are_notfound__error_raised():
    from alchemyjsonschema import SchemaFactory, ForeignKeyWalker, InvalidStatus
    from alchemyjsonschema.dictify import ModelLookup
    import alchemyjsonschema.tests.models as models
    from datetime import datetime
    import pytest
    factory = SchemaFactory(ForeignKeyWalker)
    user_schema = factory(models.User)
    created_at = datetime(2000, 1, 1)
    user_dict = dict(name='foo', created_at=created_at)
    modellookup = ModelLookup(models)
    with pytest.raises(InvalidStatus):
        _callFUT(user_dict, user_schema, modellookup, strict=True)
