#!/usr/bin/env python3
'''Module defines safely_get_value function'''
from typing import Any, Union, Mapping, TypeVar


def safely_get_value(
        dct: Mapping,
        key: Any,
        default: Union[TypeVar, None] = None
        ) -> Union[Any, TypeVar]:
    '''return dict member or default value'''
    if key in dct:
        return dct[key]
    else:
        return default
