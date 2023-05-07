import pathlib
import phantomconfig as pc
from .stub import test_data


def test_write_phantom_config():
    'Test writing Phantom config files.'
    tmp_file = pathlib.Path('tmp.in')
    conf = pc.read_config(test_phantom_file)
    conf.write_phantom(tmp_file)
    conf = pc.read_config(tmp_file)
    assert (conf.config == test_data.config)
    assert (conf.header == test_data.header)
    assert (conf.datetime == test_data._datetime)
    tmp_file.unlink()
