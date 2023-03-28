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


def _datetime(*args):
    import pytz
    from datetime import datetime
    args = list(args)
    args.append(pytz.utc)
    return datetime(*args)
