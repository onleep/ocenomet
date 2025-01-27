import asyncio

from aiocron import crontab

from .tasks import parsing


async def cron():
    crontab('0 0 * * *', func=parsing)  # 24 hours

    await asyncio.Event().wait()
