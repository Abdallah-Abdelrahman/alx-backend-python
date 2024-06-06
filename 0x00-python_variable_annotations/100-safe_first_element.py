#!/usr/bin/env python3
'''Module defines safe_first_element function'''
from typing import Any, Sequence, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    '''returns list or None'''
    if lst:
        return lst[0]
    else:
        return None
