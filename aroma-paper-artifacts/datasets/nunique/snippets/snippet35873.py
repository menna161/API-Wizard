from __future__ import print_function
import argparse
import datetime
import getpass
import logging
import sys
import time
from auvsi_suas.client.client import AsyncClient
from auvsi_suas.proto.interop_api_pb2 import Telemetry
from google.protobuf import json_format
from mavlink_proxy import MavlinkProxy
from upload_odlcs import upload_odlcs


def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s: %(name)s: %(levelname)s: %(message)s')
    parser = argparse.ArgumentParser(description='AUVSI SUAS Interop CLI.')
    parser.add_argument('--url', required=True, help='URL for interoperability.')
    parser.add_argument('--username', required=True, help='Username for interoperability.')
    parser.add_argument('--password', help='Password for interoperability.')
    subparsers = parser.add_subparsers(help='Sub-command help.')
    subparser = subparsers.add_parser('teams', help='Get the status of teams.')
    subparser.set_defaults(func=teams)
    subparser = subparsers.add_parser('mission', help='Get mission details.')
    subparser.set_defaults(func=mission)
    subparser.add_argument('--mission_id', type=int, required=True, help='ID of the mission to get.')
    subparser = subparsers.add_parser('odlcs', help='Upload odlcs.', description='Download or upload odlcs to/from the interoperability\nserver.\n\nWithout extra arguments, this prints all odlcs that have been uploaded to the\nserver.\n\nWith --odlc_dir, this uploads new odlcs to the server.\n\nThis tool searches for odlc JSON and images files within --odlc_dir\nconforming to the 2017 Object File Format and uploads the odlc\ncharacteristics and thumbnails to the interoperability server.\n\nThere is no deduplication logic. Odlcs will be uploaded multiple times, as\nunique odlcs, if the tool is run multiple times.', formatter_class=argparse.RawDescriptionHelpFormatter)
    subparser.set_defaults(func=odlcs)
    subparser.add_argument('--mission_id', type=int, help='Mission ID to restrict ODLCs retrieved.', default=None)
    subparser.add_argument('--odlc_dir', help='Enables odlc upload. Directory containing odlc data.')
    subparser = subparsers.add_parser('map', help='Upload maps.', description='Download or upload map images to/from the server.\n\nWith just the mission specified it prints the imagery data. With a image\nfilepath specified, it uploads the map to the server.', formatter_class=argparse.RawDescriptionHelpFormatter)
    subparser.set_defaults(func=maps)
    subparser.add_argument('--mission_id', type=int, help='Mission ID for the map.', required=True)
    subparser.add_argument('--map_filepath', type=str, help='Filepath to the image to upload.')
    subparser = subparsers.add_parser('probe', help='Send dummy requests.')
    subparser.set_defaults(func=probe)
    subparser.add_argument('--interop_time', type=float, default=1.0, help='Time between sent requests (sec).')
    subparser = subparsers.add_parser('mavlink', help='Receive MAVLink GLOBAL_POSITION_INT packets and\nforward as telemetry to interop server.')
    subparser.set_defaults(func=mavlink)
    subparser.add_argument('--device', type=str, help='pymavlink device name to read from. E.g. tcp:localhost:8080.')
    args = parser.parse_args()
    if args.password:
        password = args.password
    else:
        password = getpass.getpass('Interoperability Password: ')
    client = AsyncClient(args.url, args.username, password)
    args.func(args, client)
