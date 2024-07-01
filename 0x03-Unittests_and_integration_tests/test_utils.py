#!/usr/bin/env python3
'''Module defines `TestAccessNestedMap` class'''
from parameterized import parameterized
from typing import Any, Dict, Mapping, Sequence, Type, Union
import unittest
from unittest.mock import Mock, patch

from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    '''class definition.
    Methods: test_access_nested_map, test_access_nested_map_exception,
    '''
    @parameterized.expand([
        ({"a": 1}, ["a",], 1),
        ({"a": {"b": 2}}, ["a",], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2)
        ])
    def test_access_nested_map(self,
                               nested_map: Mapping,
                               path: Sequence,
                               expected: Union[Dict[str, Any], int]):
        '''test nested map with various keys'''
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({"a": 1}, ["b"], KeyError),
        ({}, ("a",), KeyError),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Mapping,
            path: Sequence,
            exception: Any) -> None:
        '''test key error for invalid keys'''
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    '''class definition to mock http calls'''
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, url: str, payload: Dict[str, bool]) -> None:
        '''mock get reqeust and ensure method called once'''
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
    '''class definition for memoization'''

    def test_memoize(self) -> None:
        '''define inner class for memoization'''

        class TestClass:
            '''inner class that has memoized method'''

            def a_method(self) -> int:
                '''method returns constant 42'''
                return 42

            @memoize
            def a_property(self) -> int:
                '''memoized method by decorator `memoized`'''
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock:
            test_instance = TestClass()

            # Assert the results are correct
            self.assertEqual(test_instance.a_property, 42)
            self.assertEqual(test_instance.a_property, 42)

            # Assert a_method was called only once
            mock.assert_called_once()
