import re
import sys
import argparse
import requests


def main():
    parser = argparse.ArgumentParser(description='Download videos from facebook from your terminal')
    parser.add_argument('url', action='store')
    parser.add_argument('resolution', action='store', nargs='?')
    args = parser.parse_args()
    print('Fetching source code...', end='\r', flush=True)
    request = requests.get(args.url)
    print(ERASE_LINE, end='\r', flush=True)
    print('\x1b[92m✔\x1b[0m Fetched source code')
    file_name = (str(re.findall('videos\\/(.+?)\\"', request.text)[(- 1)].replace('/', '')) + f"_{('sd' if (args.resolution == 'sd') else 'hd')}.mp4")
    print('Downloading video...', end='\r', flush=True)
    try:
        request = requests.get(re.findall(f"""{('sd_src' if (args.resolution == 'sd') else 'hd_src')}:"(.+?)"""", request.text)[0])
    except IndexError:
        print(ERASE_LINE, end='\r', flush=True)
        print('\\e[91m✘\\e[0m Video could not be downloaded')
        sys.exit()
    with open(file_name, 'wb') as f:
        f.write(request.content)
    print(ERASE_LINE, end='\r', flush=True)
    print(f'[92m✔[0m Video downloaded: {file_name}')
