import asyncio

from api.main import fastapi
from sheduler.crontab import cron


async def main():
    await asyncio.gather(
        # asyncio.to_thread(x()) # for sync
        asyncio.to_thread(lambda: asyncio.run(cron())),
        asyncio.to_thread(lambda: asyncio.run(fastapi())),
    )


if __name__ == "__main__":
    asyncio.run(main())
