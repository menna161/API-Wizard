import pathlib
import phantomconfig as pc
from .stub import test_data


def test_read_dict_flat():
    'Test reading flat Python dictionaries.'
    conf = pc.read_dict(test_dict_flat, dtype='flat')
    assert (conf.config == test_data.config)
    assert (conf.header == test_data.header)
    assert (conf.datetime == test_data._datetime)
