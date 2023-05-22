import docker
from docker.errors import ContainerError, ImageNotFound
from pathlib import Path
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup
from axcell.errors import LatexConversionError


def clean_html(self, path):
    path = Path(path)
    with path.open('rb') as file:
        soup = BeautifulSoup(file, 'html5lib')
    return str(soup)
