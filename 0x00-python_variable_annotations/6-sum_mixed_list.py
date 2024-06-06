#!/usr/bin/env python3
'''Module defines sum_list function'''
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    '''sum list elements.

    Return:
        float: the sum of the list
    '''
    sum = 0.0
    for n in mxd_lst:
        sum += n

    return sum
