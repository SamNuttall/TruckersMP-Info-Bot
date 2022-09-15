# Core: Log
# Provides helpful utilities for logging
import functools
import os

from core.public import logger
from timeit import default_timer


def interaction(int_type: str):
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            start = default_timer()
            ctx = args[0]
            guild = ctx.guild_id if ctx.guild_id else "N/A (Direct Msg)"
            author = ctx.author.user.id if ctx.author else "Unknown"

            try:
                result = await func(*args, **kwargs)
            finally:
                end = default_timer()

                taken_ms = round((end - start) * 1000)
                logger.debug(f"Handle {int_type.capitalize()} Interaction: {func.__name__} | "
                             f"guild: {guild}, user: {author}, time: {taken_ms}ms")
            return result

        return wrapped

    return wrapper
