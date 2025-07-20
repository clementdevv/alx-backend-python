

#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from utils import get_json


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient.org"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that org method returns correct response"""
        # Setup mock return value
        expected = {"login": org_name, "id": 12345}
        mock_get_json.return_value = expected

        # Instantiate and call the method
        client = GithubOrgClient(org_name)
        result = client.org()

        # Assertions
        self.assertEqual(result, expected)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test the _public_repos_url property"""
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        
        client = GithubOrgClient("testorg")
        result = client._public_repos_url

        self.assertEqual(result, "https://api.github.com/orgs/testorg/repos")


    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """Test GithubOrgClient.public_repos method"""
        # Setup mock values
        mock_public_repos_url.return_value = "http://example.com/repos"
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]

        client = GithubOrgClient("testorg")
        result = client.public_repos()

        # Assertions
        self.assertEqual(result, ["repo1", "repo2", "repo3"])
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with("http://example.com/repos")


    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock)
    def test_public_repos_with_license(self, mock_public_repos_url, mock_get_json):
        """Test GithubOrgClient.public_repos method with license filter"""

        mock_public_repos_url.return_value = "http://example.com/repos"
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}},
            {"name": "repo4", "license": {"key": "gpl"}},
        ]

        client = GithubOrgClient("testorg")
        result = client.public_repos(license="mit")

        # Assertions
        self.assertEqual(result, ["repo1", "repo3"])
        mock_get_json.assert_called_once_with("http://example.com/repos")
        mock_public_repos_url.assert_called_once()


