import contextvars
import functools
from asyncio import events
from concurrent.futures import ThreadPoolExecutor

__all__ = "to_thread",
executor = ThreadPoolExecutor(max_workers=50)


async def to_thread(func, /, *args, **kwargs):
    loop = events.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(executor, func_call)
