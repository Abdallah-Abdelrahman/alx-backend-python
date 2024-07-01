#!/usr/bin/env python3
'''Module defines `TestAccessNestedMap` class'''
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    '''class definition'''

    @parameterized.expand([
        ('google', {'login': 'google'}),
        ('abc', {'login': 'abc'})
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_result, mock_get_json):
        '''Test that GithubOrgClient.org returns the correct value'''
        mock_get_json.return_value = expected_result

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_result)
        mock_get_json.assert_called_once_with(
                'https://api.github.com/orgs/{}'.format(org_name))

    @patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        '''Test that GithubOrgClient._public_repos_url returns the correct URL
        '''
        mock_payload = {
            'repos_url': 'https://api.github.com/orgs/testorg/repos'
        }
        mock_org.return_value = mock_payload

        client = GithubOrgClient('testorg')
        result = client._public_repos_url

        self.assertEqual(result, mock_payload['repos_url'])
        mock_org.assert_called_once()
