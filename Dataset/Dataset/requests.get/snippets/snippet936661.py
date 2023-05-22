import progress.bar
import requests
from uiautomator2.version import __apk_version__


def download(url, target):
    print('Download', target)
    r = requests.get(url, stream=True)
    r.raise_for_status()
    bar = progress.bar.Bar()
    bar.max = int(r.headers.get('content-length'))
    with open(target, 'wb') as f:
        for chunk in r.iter_content(chunk_size=4096):
            f.write(chunk)
            bar.next(len(chunk))
        bar.finish()
