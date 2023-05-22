import asyncio
import datetime
import json
import logging
from concurrent import futures
import aiohttp
import pytest
from google.cloud import pubsub
from gordon_gcp.clients import auth
from gordon_gcp.plugins.service import event_consumer


@classmethod
def utcnow(cls):
    return datetime.datetime(2018, 1, 1, 11, 30, 0)
