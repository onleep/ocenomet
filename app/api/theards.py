import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial

executor = ThreadPoolExecutor(max_workers=50)


async def to_thread(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    func_with_kwargs = partial(func, **kwargs)
    return await loop.run_in_executor(executor, func_with_kwargs, *args)
