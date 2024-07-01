#!/usr/bin/env python3
'''Module defines `TestAccessNestedMap` class'''
import unittest
from unittest.mock import patch, Mock
from typing import Mapping, Sequence, Type
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


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


class TestGetJson(unittest.TestCase):
    '''class definition'''
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, url, payload):
        '''mock get reqeust'''
        mock_response = Mock()
        mock_response.json.return_value = payload

        with patch('utils.requests.get', return_value=mock_response) as mock:
            # Call the function
            result = get_json(url)

            # Check that requests.get was called once with the test_url
            mock.assert_called_once_with(url)

            # Check that the result is as expected
            self.assertEqual(result, payload)


class TestMemoize(unittest.TestCase):
    '''class definition'''
    def test_memoize(self) -> None:
        '''define inner class for memoization'''
        class TestClass:
            '''inner class'''
            def a_method(self) -> int:
                '''return 42'''
                return 42

            @memoize
            def a_property(self) -> int:
                '''memoized method'''
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock:
            test_instance = TestClass()

            # Call a_property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Assert the results are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert a_method was called only once
            mock.assert_called_once()
