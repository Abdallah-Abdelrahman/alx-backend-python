#!/usr/bin/env python3
'''Module defines `TestAccessNestedMap` class'''
from typing import Mapping, Sequence, Type
import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    '''class definition'''
    @parameterized.expand([
        ({"a": 1}, ["a",], 1),
        ({"a": {"b": 2}}, ["a",], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2)
        ])
    def test_access_nested_map(self, nested_map, path, expected):
        '''test nested map'''
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({"a": 1}, ["b"], KeyError),
        ({}, ("a",), KeyError),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Mapping,
            path: Sequence,
            exception: Type[BaseException]) -> None:
        '''test key error'''
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)
