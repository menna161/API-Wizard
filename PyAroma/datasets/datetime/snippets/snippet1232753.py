import pathlib
import phantomconfig as pc
from .stub import test_data


def test_read_phantom_config():
    'Test reading Phantom config files.'
    conf = pc.read_config(test_phantom_file)
    assert (conf.config == test_data.config)
    assert (conf.header == test_data.header)
    assert (conf.datetime == test_data._datetime)
