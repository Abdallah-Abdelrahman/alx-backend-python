#!/usr/bin/env python3
'''Module defines coroutines `wait_random`'''
import asyncio
import random


async def wait_random(max_delay: int = 10):
    '''random delay between 0 and max_delay'''
    i = random.uniform(0, max_delay)
    await asyncio.sleep(i)
    return i
