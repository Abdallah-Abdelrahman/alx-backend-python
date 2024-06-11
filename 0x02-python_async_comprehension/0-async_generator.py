#!/usr/bin/env python3
'''Module defines `async_generator`'''
from typing import Generator
import asyncio
import random


async def async_generator() -> Generator[float, None, None]:
    '''coroutine will loop 10 times.

    Yields:
        float: between 0 and 10
    '''
    i = 0

    while i < 10:
        n = random.uniform(0, 10)
        await asyncio.sleep(1)
        yield n
        i += 1
