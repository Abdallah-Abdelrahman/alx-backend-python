#!/usr/bin/env python3
'''Module defines to_kv function'''
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    def mutliply(n):
        return n * multiplier
    return mutliply
