#!/usr/bin/env python3
'''Module defines `TestAccessNestedMap` class'''
from typing import Any, Dict
from unittest import TestCase
from unittest.mock import MagicMock, Mock, PropertyMock, patch
from parameterized import parameterized, parameterized_class
from requests import HTTPError
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


PAYLOAD = {
            'repos_url': 'https://api.github.com/orgs/google/repos',
            'repos': [
                {
                    'id': 7697149,
                    'node_id': 'MDEwOlJlcG9zaXRvcnk3Njk3MTQ5',
                    'name': 'episodes.dart',
                    'full_name': 'google/episodes.dart',
                    'private': False,
                    'forks': 22,
                    'open_issues': 0,
                    'watchers': 12,
                    'default_branch': 'master',
                    'permissions': {
                        'admin': False,
                        'push': False,
                        'pull': True
                    },
                },
                {
                    'id': 7776515,
                    'node_id': 'MDEwOlJlcG9zaXRvcnk3Nzc2NTE1',
                    'name': 'cpp-netlib',
                    'full_name': 'google/cpp-netlib',
                    'private': False,
                    'forks': 59,
                    'open_issues': 0,
                    'watchers': 292,
                    'default_branch': 'master',
                    'permissions': {
                        'admin': False,
                        'push': False,
                        'pull': True
                    },
                },
            ],
}


class TestGithubOrgClient(TestCase):
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

    def test_public_repos_url(self):
        '''Test that GithubOrgClient._public_repos_url returns the correct URL
        '''
        with patch(
            'client.GithubOrgClient.org', new_callable=PropertyMock
        ) as mocked_property:
            mocked_property.return_value = {
                'repos_url': 'https://api.github.com/orgs/google/repos'
            }
            self.assertEqual(
                GithubOrgClient('google')._public_repos_url,
                'https://api.github.com/orgs/google/repos',
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: MagicMock):
        '''Test GithubOrgClient.public_repos'''
        mock_get_json.return_value = PAYLOAD['repos']

        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=PropertyMock
                          ) as mock_public_repos_url:
            mock_public_repos_url.return_value =\
                    'https://api.github.com/orgs/testorg/repos'

            client = GithubOrgClient('testorg')
            result = client.public_repos()

            self.assertEqual(result, ['episodes.dart', 'cpp-netlib'])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                    'https://api.github.com/orgs/testorg/repos')

    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False),
        ({}, 'my_license', False)
    ])
    def test_has_license(self,
                         repo: Dict[str, Any],
                         license_key: str,
                         expected_result: bool):
        '''Test GithubOrgClient.has_license'''
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


@parameterized_class(('org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'),
                     TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(TestCase):
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
