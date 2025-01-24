import asyncio

from api.main import fastapi
from sheduler.crontab import cron


async def main():
    await asyncio.gather(fastapi(), cron())


if __name__ == "__main__":
    asyncio.run(main())
