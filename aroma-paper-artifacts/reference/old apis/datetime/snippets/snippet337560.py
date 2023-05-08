from .utils import *


def test_basic_serialisation():
    p = create_rich_project()
    p.finalise_and_validate()
    print('\n> serialized project: {}'.format(p.dumps(pretty_print=True)))
    deserialised_proj = Project.loads(p.dumps())
    print('> deserialized project: {}'.format(deserialised_proj))
    assert (type(deserialised_proj.created) == datetime)
    assert (deserialised_proj.created == p.created), '!!! the deserialized project has created field w. type {} while it should be {}'.format(type(deserialised_proj.created), type(p.created))
