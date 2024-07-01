#!/usr/bin/env python3
'''Module defines `TestAccessNestedMap` class'''
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
        ({"a": 1}, ["b"], "b")
    ])
    def test_access_nested_map_exception(self, nested_map, path, key):
        '''test key error'''
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
        self.assertEqual(str(e.exception), f"'{key}'")
