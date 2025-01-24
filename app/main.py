import asyncio

import uvicorn
from sheduler.crontab import cron


async def main():
    uvicorn.run('api.main:app', host='0.0.0.0', log_config=None)
    await cron()


if __name__ == "__main__":
    asyncio.run(main())
