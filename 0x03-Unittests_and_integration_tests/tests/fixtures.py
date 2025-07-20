
# tests/fixtures.py
from typing import Dict

ORG_PAYLOAD: Dict = {
    "login": "google",
    "id": 1342004,
    "url": "https://api.github.com/orgs/google"
}

REPOS_PAYLOAD: Dict = [
    {
        "id": 1,
        "name": "repo1",
        "license": {"key": "mit"}
    },
    {
        "id": 2,
        "name": "repo2",
        "license": {"key": "apache-2.0"}
    }
]
