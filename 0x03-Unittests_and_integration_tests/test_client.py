#!/usr/bin/env python3
"""test_client.py
    This module contains the test cases for the client module
"""
from parameterized import parameterized, parameterized_class
import unittest
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """ TestGithubOrgClient class
    """
    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch('client.get_json')
    def test_org(self, org, mock_get_json):
        """ Test org method
        """
        test_client = GithubOrgClient(org)
        test_client.org()
        url = f"https://api.github.com/orgs/{org}"
        mock_get_json.assert_called_once_with(url)

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    def test_public_repos_url(self, org):
        """ Test _public_repos_url method
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock,
                   return_value={"repos_url": "http://example.com"}
                   ):
            test_client = GithubOrgClient(org)
            self.assertEqual(test_client._public_repos_url,
                             "http://example.com")

    @patch('client.get_json', return_value=[{"name": "Google"},
                                            {"name": "abc"}])
    def test_public_repos(self, mock_get_json):
        """ Test public_repos method
        """
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock,
                   return_value="http://example.com"
                   ) as mock_public_repos_url:
            test_client = GithubOrgClient("google")
            expected = [item["name"] for item in mock_get_json.return_value]
            self.assertEqual(test_client.public_repos(), expected)

        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """ unit-test for GithubOrgClient.has_license """
        test_client = GithubOrgClient('google')
        result = test_client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(('org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'),
                     TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    ''' TestIntegrationGithubOrgClient class
        Test the integration of the GithubOrgClient class
        By mocking the requests.get method
    '''
    @classmethod
    def setUpClass(cls):
        ''' Set up class
        '''
        def side_effect(url: str):
            '''
            This is a side effect method to be added to the requests.get
            mock to return a mock response with certain attributes
            '''
            response_mock = Mock()
            if url == 'https://api.github.com/orgs/google':
                response_mock.json.side_effect = lambda: cls.org_payload
            elif url == 'https://api.github.com/orgs/google/repos':
                response_mock.json.side_effect = lambda: cls.repos_payload
            else:
                response_mock.json.side_effect = lambda: None
            return response_mock

        cls.get_patcher = patch('requests.get', side_effect=side_effect)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        ''' Tear down class
        '''
        cls.get_patcher.stop()

    def test_public_repos(self):
        ''' Integration test: public repos'''
        test_class = GithubOrgClient('google')

        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos('SomeLicence'), [])
        self.mock_get.assert_called()

    def test_public_repos_with_license(self):
        ''' Integration test for public repos with License '''
        test_class = GithubOrgClient('google')

        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos('SomeLicence'), [])
        self.assertEqual(
                test_class.public_repos('apache-2.0'), self.apache2_repos)
        self.mock_get.assert_called()
