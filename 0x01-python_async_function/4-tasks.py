#!/usr/bin/env python3
'''Module defines coroutines `task_wait_n`'''
from typing import List
wait_n = __import__('1-concurrent_coroutines').wait_n


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    '''return the list of all the delays (float values)'''
    return await (wait_n(n, max_delay))
