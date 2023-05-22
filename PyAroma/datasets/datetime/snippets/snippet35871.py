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


def probe(args, client):
    while True:
        start_time = datetime.datetime.now()
        telemetry = Telemetry()
        telemetry.latitude = 0
        telemetry.longitude = 0
        telemetry.altitude = 0
        telemetry.heading = 0
        client.post_telemetry(telemetry).result()
        end_time = datetime.datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        logger.info('Executed interop. Total latency: %f', elapsed_time)
        delay_time = (args.interop_time - elapsed_time)
        if (delay_time > 0):
            try:
                time.sleep(delay_time)
            except KeyboardInterrupt:
                sys.exit(0)
