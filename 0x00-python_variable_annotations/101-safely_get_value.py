#!/usr/bin/env python3
'''Module defines safely_get_value function

Attrs:
    T: generic type
'''
from typing import Any, Union, Mapping, TypeVar


T = TypeVar('T')


def safely_get_value(
        dct: Mapping,
        key: Any,
        default: Union[T, None] = None
        ) -> Union[Any, T]:
    '''return dict member or default value'''
    if key in dct:
        return dct[key]
    else:
        return default
