#!/usr/bin/env python3
'''Module defines coroutines `wait_random`'''
import asyncio
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    '''return the list of all the delays (float values)'''
    res = await asyncio.gather(*(wait_random(max_delay) for _ in range(n)))
    return sorted(res)
