#!/usr/bin/env python3
'''Module defines sum_list function'''
from typing import List


def sum_list(input_list: List[float]) -> float:
    '''sum list elements

    Returns:
        float: the sum
    '''
    sum = 0.0
    for n in input_list:
        sum += n
    return sum
