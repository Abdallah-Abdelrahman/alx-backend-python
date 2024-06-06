#!/usr/bin/env python3
'''Module defines to_kv function'''
from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple:
    '''returns tuple'''
    return (k, v ** 2)
