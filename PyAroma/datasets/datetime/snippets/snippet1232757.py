import pathlib
import phantomconfig as pc
from .stub import test_data


def test_read_dict_nested():
    'Test reading nested Python dictionaries.'
    conf = pc.read_dict(test_dict_nested, dtype='nested')
    assert (conf.config == test_data.config)
    assert (conf.header == test_data.header)
    assert (conf.datetime == test_data._datetime)
