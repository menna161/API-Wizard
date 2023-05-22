import os
import sys
import time
import argparse
import concurrent.futures as futures
import requests
from PIL import Image
from tqdm import tqdm
from robosat.tiles import tiles_from_csv, fetch_image


def main(args):
    tiles = list(tiles_from_csv(args.tiles))
    with requests.Session() as session:
        num_workers = args.rate
        progress = tqdm(total=len(tiles), ascii=True, unit='image')
        with futures.ThreadPoolExecutor(num_workers) as executor:

            def worker(tile):
                tick = time.monotonic()
                (x, y, z) = map(str, [tile.x, tile.y, tile.z])
                os.makedirs(os.path.join(args.out, z, x), exist_ok=True)
                path = os.path.join(args.out, z, x, '{}.{}'.format(y, args.ext))
                if os.path.isfile(path):
                    return (tile, True)
                url = args.url.format(x=tile.x, y=tile.y, z=tile.z)
                res = fetch_image(session, url)
                if (not res):
                    return (tile, False)
                try:
                    image = Image.open(res)
                    image.save(path, optimize=True)
                except OSError:
                    return (tile, False)
                tock = time.monotonic()
                time_for_req = (tock - tick)
                time_per_worker = (num_workers / args.rate)
                if (time_for_req < time_per_worker):
                    time.sleep((time_per_worker - time_for_req))
                progress.update()
                return (tile, True)
            for (tile, ok) in executor.map(worker, tiles):
                if (not ok):
                    print('Warning: {} failed, skipping'.format(tile), file=sys.stderr)
