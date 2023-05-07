import discord
from discord.ext import commands
import datetime
import os
import aiohttp
import asyncio
from .utils import images
from io import BytesIO
import logging
from yarl import URL


def cog_unload(self):
    logger.info('die')
    utcnow = datetime.datetime.utcnow()
    self.post_avy_task.cancel()
    self.dl_avys_task.cancel()
    self.batch_remove_task.cancel()
    for (recordtype, task) in self.bg_tasks.items():
        logger.info(f'canceling {recordtype}')
        task.cancel()
    self.bot.loop.create_task(self.cog_log(False, utcnow))
