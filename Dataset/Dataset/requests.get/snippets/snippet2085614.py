import requests
import argparse
import shutil
import os
import re
import json


def download_user_pages(username, pagetype):
    'Download paged metadata from user (projects, favorites, followers etc)'
    offset = 0
    try:
        downloadedcontent = []
        while True:
            print(f"Downloading {username}'s {pagetype} (page {(offset + 1)})")
            r = requests.get(f'https://api.scratch.mit.edu/users/{username}/{pagetype}?limit=20&offset={(offset * 20)}', headers=headers)
            content = json.loads(r.content)
            if (len(content) == 0):
                break
            downloadedcontent += content
            offset += 1
        if os.path.exists(f'{pagetype}.json'):
            with open(f'{pagetype}.json', 'r', encoding='UTF-8') as f:
                oldcontent = json.load(f)
            existingids = []
            for x in downloadedcontent:
                existingids.append(x['id'])
            for x in oldcontent:
                if (not (x['id'] in existingids)):
                    downloadedcontent.append(x)
        with open(f'{pagetype}.json', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(downloadedcontent))
        return downloadedcontent
    except:
        print(f"Error downloading {username}'s {pagetype}")
        with open('error.log', 'a', encoding='UTF-8') as f:
            f.write(f'''Error downloading {username}'s {pagetype}
''')
        return []
