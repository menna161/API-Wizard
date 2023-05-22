from pathlib import Path
from setuptools import setup
import requests
from tools import release


def fetch_vue_cli_js_file(source: str, name: str) -> str:
    js_data_base = ((Path(__file__).parent / 'vuecli') / 'js')
    js_data_base.mkdir(exist_ok=True)
    dest_path = (js_data_base / name)
    resp = requests.get(source)
    assert resp.ok
    dest_path.write_bytes(resp.content)
    return f'js/{name}'
