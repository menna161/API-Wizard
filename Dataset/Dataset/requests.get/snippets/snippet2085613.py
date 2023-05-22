import requests
import argparse
import shutil
import os
import re
import json


def download_project(project_id):
    'Download project'
    project_id = str(int(project_id))
    print(f'Downloading project {project_id}')
    r = requests.get(f'https://projects.scratch.mit.edu/{project_id}', headers=headers)
    version = 0
    if (r.content[:9] == b'ScratchV0'):
        version = 1
        with open(f'{project_id}.sb', 'wb') as f:
            f.write(r.content)
        return {'success': True, 'version': version}
    if (not os.path.exists(project_id)):
        os.mkdir(project_id)
    with open(f'{project_id}/project.json', 'wb') as f:
        f.write(r.content)
    project_json = json.loads(r.content)
    if ('info' in project_json):
        version = 2
        counter = 0
        if ('penLayerMD5' in project_json):
            if (len('penLayerMD5') > 0):
                project_json['penLayerID'] = counter
                download_asset_c(project_json['penLayerMD5'], counter, project_id)
                counter += 1
        if ('sounds' in project_json):
            for sound in project_json['sounds']:
                sound['soundID'] = counter
                download_asset_c(sound['md5'], counter, project_id)
                counter += 1
        if ('costumes' in project_json):
            for costume in project_json['costumes']:
                costume['baseLayerID'] = counter
                download_asset_c(costume['baseLayerMD5'], counter, project_id)
                counter += 1
        for child in project_json['children']:
            if ('penLayerMD5' in child):
                if (len('penLayerMD5') > 0):
                    child['penLayerID'] = counter
                    download_asset_c(child['penLayerMD5'], counter, project_id)
                    counter += 1
            if ('sounds' in child):
                for sound in child['sounds']:
                    sound['soundID'] = counter
                    download_asset_c(sound['md5'], counter, project_id)
                    counter += 1
            if ('costumes' in child):
                for costume in child['costumes']:
                    costume['baseLayerID'] = counter
                    download_asset_c(costume['baseLayerMD5'], counter, project_id)
                    counter += 1
        os.rename(f'{project_id}/project.json', f'{project_id}/original.json')
        with open(f'{project_id}/project.json', 'w', encoding='UTF-8') as f:
            json.dump(project_json, f)
    else:
        version = 3
        for target in project_json['targets']:
            for k in ['costumes', 'sounds']:
                if (k in target):
                    for item in target[k]:
                        download_asset(item['md5ext'], project_id)
    shutil.make_archive(f'{project_id}', 'zip', project_id)
    os.rename(f'{project_id}.zip', f'{project_id}.sb{str(version)}')
    shutil.rmtree(project_id)
    return {'success': True, 'version': version}
