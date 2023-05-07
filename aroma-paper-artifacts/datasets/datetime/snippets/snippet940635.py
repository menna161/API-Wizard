import types as _types
import typing as T
import datetime
import inspect
from . import helpers
from . import types
from .. import schedule
from ..room import Room


def build_expr_env(room: 'Room', now: datetime.datetime) -> T.Dict[(str, T.Any)]:
    "This function builds and returns an environment usable as globals\n    for the evaluation of an expression.\n    It will add all members of the .types module's __all__ to the\n    environment.\n    Additionally, helpers provided by the .helpers module and the actor\n    type will be constructed based on the Room object"
    env = {}
    for member_name in types.__all__:
        env[member_name] = getattr(types, member_name)
    helper_types = []
    for (member_name, member) in inspect.getmembers(helpers):
        if ((member is not helpers.HelperBase) and isinstance(member, type) and issubclass(member, helpers.HelperBase)):
            helper_types.append(member)
    assert (room.app.actor_type is not None)
    helper_types.extend(room.app.actor_type.expression_helpers)
    helper_types.sort(key=(lambda t: t.order))
    for helper_type in helper_types:
        room.log('Initializing expression helper: {}, order = {}'.format(helper_type.__name__, helper_type.order), level='DEBUG')
        helper = helper_type(room, now, env)
        helper.update_environment()
    return env
