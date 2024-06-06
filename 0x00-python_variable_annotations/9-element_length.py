#!/usr/bin/env python3
'''Module defines element_length function'''
from typing import List, Iterable, Sequence, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    '''returns iterable'''
    return [(i, len(i)) for i in lst]
