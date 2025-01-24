from aiocron import crontab

from .process import parsing


async def cron():

    crontab('0 0 * * *', func=parsing)  # 24 hours
