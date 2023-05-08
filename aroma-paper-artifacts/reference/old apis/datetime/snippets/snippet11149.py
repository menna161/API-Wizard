from datetime import datetime, timedelta
from adjax.registry import registry
from adjax.utils.types import typed
from .models import CustomObject


@registry.register
@typed({'some_date': datetime, 'return': datetime})
def func3(request, some_date):
    return (some_date + timedelta(days=2))
