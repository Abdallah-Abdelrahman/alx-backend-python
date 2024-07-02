#!/usr/bin/env python3
'''Module defines:
`TestAccessNestedMap`, `TestGetJson`, `TestMemoize`
classes.
'''
from parameterized import parameterized
import requests
from typing import Any, Dict, List, Union
import unittest
from unittest.mock import patch, Mock
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
                               nested_map: Dict[str, Any],
                               path: List[str],
                               expected: Union[Dict[str, Any], int]) -> None:
        '''test nested map with various keys'''
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ["a"], KeyError),
        ({"a": 1}, ["a", "b"], KeyError),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Dict[str, Any],
            path: List[str],
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
        '''mock get reqeust and ensure method called once
        Args:
            url:
            payload:
        '''
        mock_response = Mock()
        mock_response.json.return_value = payload

        with patch.object(requests,
                          'get',
                          return_value=mock_response) as mock:
            # Call the function
            result = get_json(url)

            # Check that the result is as expected
            self.assertEqual(result, payload)

        # Check that requests.get was called once
        mock.assert_called_once()


class TestMemoize(unittest.TestCase):
    ''' Test the memoize method
        Methods:
            test_memoize - test the memoize method, which caches the output of
            a method
    '''
    def test_memoize(self) -> None:
        '''
            Test the memoize method
            The memoize method should cache the output of a method
            Calls to the method with the same arguments should return
            the cached output

            Class TestClass has a method a_method that returns 42
            Class TestClass has a property a_property that is memoized
            Calls to a_property should return 42
        '''

        class TestClass:
            ''' TestClass with a_method and a_property
            '''
            def a_method(self) -> int:
                ''' a_method that returns 42
                '''
                return 42

            @memoize
            def a_property(self) -> int:
                ''' a_property that is memoized
                '''
                return self.a_method()

        test = TestClass()
        with patch.object(TestClass, 'a_method',
                          wraps=test.a_method) as mock_method:
            out1 = test.a_property
            out2 = test.a_property
            self.assertEqual(out1, 42)
            self.assertEqual(out2, 42)
            mock_method.assert_called_once()
