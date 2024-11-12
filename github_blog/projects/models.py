from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    repo_name = models.CharField(max_length=255)  # GitHub repository name

    def __str__(self):
        return f"{self.name} ({self.repo_name})"

class WikiPage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="wiki_pages")
    title = models.CharField(max_length=255)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.project.name}"
