import requests
import argparse
import shutil
import os
import re
import json


def download_user(username):
    'Download user account with metadata and projects'
    print(f'Downloading user {username}')
    if (not os.path.exists(username)):
        os.mkdir(username)
    os.chdir(username)
    r = requests.get(f'https://api.scratch.mit.edu/users/{username}', headers=headers)
    userid = json.loads(r.content)['id']
    with open(f'userinfo.json', 'wb') as f:
        f.write(r.content)
    download_file(f'https://cdn2.scratch.mit.edu/get_image/user/{userid}_100000x100000.png', 'avatar.png')
    download_user_pages(username, 'favorites')
    download_user_pages(username, 'following')
    download_user_pages(username, 'followers')
    projects = download_user_pages(username, 'projects')
    for project in projects:
        download_project_and_metadata(project['id'])
    os.chdir('..')
