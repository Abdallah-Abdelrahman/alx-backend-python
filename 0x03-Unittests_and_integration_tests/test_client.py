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

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        '''Test GithubOrgClient.public_repos'''
        mock_repos_payload = [
            {'name': 'repo1'},
            {'name': 'repo2'},
            {'name': 'repo3'}
        ]
        mock_get_json.return_value = mock_repos_payload

        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=PropertyMock
                          ) as mock_public_repos_url:
            mock_public_repos_url.return_value =\
                    'https://api.github.com/orgs/testorg/repos'

            client = GithubOrgClient('testorg')
            result = client.public_repos()

            self.assertEqual(result, ['repo1', 'repo2', 'repo3'])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                    'https://api.github.com/orgs/testorg/repos')

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_result):
        '''Test GithubOrgClient.has_license'''
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)
