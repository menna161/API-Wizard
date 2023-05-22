import argparse
import json
import os
import sys
import lxml.html as html
import requests


def fetch_boards(boards, force_update=False, path=None):
    'Download board image data.\n\n    Fetches all images, downloads and writes to disk.\n    Progress is logged to terminal.\n\n    Args:\n        boards (list(dict)): board image data.\n        force_update (bool): re-download existing.\n        path (str): path in the form "user/board/section".\n    '
    images_by_directory = {}
    (_, _, filter_section) = (path.split('/') + [None, None, None])[:3]
    for board in boards:
        save_dir = os.path.join('images', os.path.join(*board['url'][1:(- 1)].split('/')))
        images_by_directory[save_dir] = fetch_images('https://www.pinterest.com/resource/BoardFeedResource/get/', board['url'], {'board_id': board['id'], 'page_size': 25})
        for (section, section_id) in (board.get('sections') or ()):
            if (filter_section and (filter_section != section)):
                continue
            save_dir = os.path.join('images', os.path.join(*board['url'][1:(- 1)].split('/')), section)
            images_by_directory[save_dir] = fetch_images('https://www.pinterest.com/resource/BoardSectionPinsResource/get', board['url'], {'section_id': section_id, 'page_size': 25})
        for (i, (save_dir, images)) in enumerate(images_by_directory.items(), 1):
            pinterest_path = '/'.join(save_dir.split(os.path.sep)[1:])
            try:
                os.makedirs(save_dir)
            except OSError as _:
                pass
            print('[{}/{}] board: {}, found {} images'.format(i, len(images), pinterest_path, len(images)))
        for (save_dir, images) in images_by_directory.items():
            for (i, image) in enumerate(images, 1):
                image_id = image['id']
                if ('images' in image):
                    url = image['images']['orig']['url']
                    basename = os.path.basename(url)
                    (_, ext) = basename.split('.')
                    file_path = os.path.join(save_dir, '{}.{}'.format(str(image_id), ext))
                    if ((not os.path.exists(file_path)) or force_update):
                        response = requests.get(url, stream=True)
                        with open(file_path, 'wb') as img:
                            for chunk in response:
                                img.write(chunk)
                else:
                    print('\nno image found: {}'.format(image_id))
                    continue
                print_progress_bar(i, len(images), prefix='Progress:', suffix='Complete', length=50)
        print()
