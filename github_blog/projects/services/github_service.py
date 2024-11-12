# projects/services/github_service.py
import requests
from django.conf import settings

class GitHubService:
    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.headers = {
            "Authorization": f"token {settings.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_wiki_pages(self, owner, repo):
        """Fetch wiki pages using the GitHub API"""
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/contents/wiki"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
