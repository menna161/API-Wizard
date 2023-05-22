import requests
import zipfile
import os


def download_file_from_google_drive(file_id, destination):
    URL = 'https://drive.google.com/uc?export=download'
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)
    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    save_response_content(response, destination)
