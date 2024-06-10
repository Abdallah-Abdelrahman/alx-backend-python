#!/usr/bin/env python3
'''Module defines coroutines `task_wait_random`'''
import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random

def measure_time(max_delay: int) -> asyncio.Task:
    '''create task to be scheduled'''
    return asyncio.create_task(wait_random(max_delay))
