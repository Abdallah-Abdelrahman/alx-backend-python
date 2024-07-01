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
            "repos_url": "https://api.github.com/orgs/google/repos",
            "repos": [
                {
                    "id": 7697149,
                    "node_id": "MDEwOlJlcG9zaXRvcnk3Njk3MTQ5",
                    "name": "episodes.dart",
                    "full_name": "google/episodes.dart",
                    "private": False,
                    "forks": 22,
                    "open_issues": 0,
                    "watchers": 12,
                    "default_branch": "master",
                    "permissions": {
                        "admin": False,
                        "push": False,
                        "pull": True
                    },
                },
                {
                    "id": 7776515,
                    "node_id": "MDEwOlJlcG9zaXRvcnk3Nzc2NTE1",
                    "name": "cpp-netlib",
                    "full_name": "google/cpp-netlib",
                    "private": False,
                    "forks": 59,
                    "open_issues": 0,
                    "watchers": 292,
                    "default_branch": "master",
                    "permissions": {
                        "admin": False,
                        "push": False,
                        "pull": True
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
            "client.GithubOrgClient.org", new_callable=PropertyMock
        ) as mocked_property:
            mocked_property.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                "https://api.github.com/orgs/google/repos",
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
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False)
    ])
    def test_has_license(self,
                         repo: Dict[str, Any],
                         license_key: str,
                         expected_result: bool):
        '''Test GithubOrgClient.has_license'''
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(TestCase):
    '''Integration tests for the GithubOrgClient class.'''

    @classmethod
    def setUpClass(cls) -> None:
        '''Set up the tests class'''
        cls.route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        cls.get_patcher = patch('requests.get', side_effect=cls.get_payload)
        cls.get_patcher.start()

        cls.client = GithubOrgClient('google')

    @classmethod
    def get_payload(cls, url: str) -> Mock:
        '''Return mock http call'''
        if url in cls.route_payload:
            return Mock(json=lambda: cls.route_payload[url])
        raise HTTPError

    @classmethod
    def tearDownClass(cls) -> None:
        '''Clean up the test class'''
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        '''Tests the public_repos method.'''
        self.assertEqual(self.client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        '''Tests the public_repos method with a license.'''
        self.assertEqual(self.client.public_repos(license='apache-2.0'),
                         self.apache2_repos,
                         )
