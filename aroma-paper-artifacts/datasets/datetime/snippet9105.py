from discord.ext import commands
import discord
import datetime
import logging
import json
import asyncio
import aiohttp
import asyncpg
import sys


def converter(data):
    if isinstance(data, datetime.datetime):
        return data.__str__()
