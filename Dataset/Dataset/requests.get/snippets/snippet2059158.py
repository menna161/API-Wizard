import os
import zipfile
import subprocess
import requests


def _main():
    include_dir_path = os.path.abspath(os.path.dirname(__file__))
    cwd = os.getcwd()
    os.chdir(include_dir_path)
    third_party_dir = os.path.join('..', '3rd_party')
    openface_filename = os.path.basename(OPENFACE)
    openface_dirname = os.path.splitext(openface_filename)[0]
    openface_local_path = os.path.join(third_party_dir, openface_dirname)
    if (not os.path.exists(openface_local_path)):
        print('Downloading OpenFace')
        response = requests.get(OPENFACE)
        with open(openface_filename, 'wb') as fp:
            fp.write(response.content)
        print('Extracting OpenFace')
        os.makedirs(third_party_dir, exist_ok=True)
        with zipfile.ZipFile(openface_filename, 'r') as zip_ref:
            zip_ref.extractall(third_party_dir)
        print('Downloading patch experts')
        os.chdir(openface_local_path)
        subprocess.run(['powershell.exe', './download_models.ps1'])
    os.chdir(cwd)
