import pathlib
import phantomconfig as pc
from .stub import test_data


def test_write_json_config():
    'Test writing JSON config files.'
    tmp_file = pathlib.Path('tmp.json')
    conf = pc.read_config(test_phantom_file)
    conf.write_json(tmp_file)
    conf = pc.read_json(tmp_file)
    assert (conf.config == test_data.config)
    assert (conf.header == test_data.header)
    assert (conf.datetime == test_data._datetime)
    tmp_file.unlink()
