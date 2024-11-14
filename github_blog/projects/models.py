# projects/models.py

from django.conf import settings
from django.db import models

class Repository(models.Model):
    name = models.CharField(max_length=100)  # Repository name (e.g., "username/reponame")
    token = models.CharField(max_length=255, help_text="Personal access token for GitHub API access")
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='repositories')

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class UserGroupSelection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.group.name}"
