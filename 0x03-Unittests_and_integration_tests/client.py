# client.py
from utils import get_json


class GithubOrgClient:
    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name):
        self.org_name = org_name

    def org(self):
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self):
        return self.org.get("repos_url")

    def public_repos(self):
        url = self._public_repos_url
        return [repo["name"] for repo in get_json(url)]
    
    def public_repos(self, license=None):
        url = self._public_repos_url
        repos = get_json(url)
        if license is None:
            return [repo["name"] for repo in repos]
        return [
            repo["name"]
            for repo in repos
            if repo.get("license", {}).get("key") == license
        ]
