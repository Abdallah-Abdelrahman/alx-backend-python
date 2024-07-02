#!/usr/bin/env python3
"""test_utils.py
   This module contains the test cases for the utils module
"""
from parameterized import parameterized
import requests
from typing import Any, Dict, List, Union
import unittest
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
        Test the access_nested_map method
        Methods:
            test_access_nested_map - test the access_nested_map method, which
            returns the value of a nested map given a list of keys to traverse
            the map
            test_access_nested_map_exception - test the access_nested_map
            method when a key is not found in the nested map
    """
    @parameterized.expand([
        ({'a': 1}, ['a'], 1),
        ({'a': {'b': 2}}, ['a'], {'b': 2}),
        ({'a': {'b': 2}}, ['a', 'b'], 2)
    ])
    def test_access_nested_map(self, nested_map: Dict[str, Any],
                               path: List[str], expected: Union[Dict[str, Any],
                                                                int]) -> None:
        """
            Test the access_nested_map method
            Args:
                nested_map: a nested map
                path: a list of keys to traverse the nested map
                expected: the expected value of the nested map
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ['a'], KeyError),
        ({'a': 1}, ['a', 'b'], KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map: Dict[str, Any],
                                         path: List[str],
                                         expected: Any) -> None:
        """
            Test the access_nested_map method
            Args:
                nested_map: a nested map with no key
                path: a list of keys to traverse the nested map
                expected: the expected exception
        """
        with self.assertRaises(expected):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test the get_json method
        Methods:
            test_get_json - test the get_json method, which returns the
            payload of a request
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str,
                      test_payload: Dict[str, bool]) -> None:
        """test_get_json method
            to test that utils.get_json returns the expected result.
            Args:
                test_url: a url
                test_payload: a payload
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        with patch.object(requests, 'get',
                          return_value=mock_response) as mock_method:
            test_response = get_json(test_url)
            self.assertEqual(test_response, test_payload)

        mock_method.assert_called_once()


class TestMemoize(unittest.TestCase):
    """ Test the memoize method
        Methods:
            test_memoize - test the memoize method, which caches the output of
            a method
    """
    def test_memoize(self) -> None:
        """
            Test the memoize method
            The memoize method should cache the output of a method
            Calls to the method with the same arguments should return
            the cached output

            Class TestClass has a method a_method that returns 42
            Class TestClass has a property a_property that is memoized
            Calls to a_property should return 42
        """

        class TestClass:
            """ TestClass with a_method and a_property
            """
            def a_method(self) -> int:
                """ a_method that returns 42
                """
                return 42

            @memoize
            def a_property(self) -> int:
                """ a_property that is memoized
                """
                return self.a_method()

        test = TestClass()
        with patch.object(TestClass, 'a_method',
                          wraps=test.a_method) as mock_method:
            out1 = test.a_property
            out2 = test.a_property
            self.assertEqual(out1, 42)
            self.assertEqual(out2, 42)
            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
