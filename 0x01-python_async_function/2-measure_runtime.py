#!/usr/bin/env python3
'''Module defines coroutines `measure_time`'''
import asyncio
import time

wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    '''measure time of execution'''
    start = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    return time.perf_counter() - start
