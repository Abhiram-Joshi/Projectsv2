from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class ContibutorModel(models.Model):
    github_username = models.CharField(max_length=50)
    profile_url = models.URLField()
    avatar_url = models.URLField()

class ProjectModel(models.Model):
    repo_name = models.CharField(max_length=100, unique=True)
    repo_api_url = models.URLField()
    repo_html_url = models.URLField()
    repo_description = models.TextField(default="", null=True)
    repo_languages = ArrayField(models.CharField(max_length=20), null=True)
    repo_issues = models.IntegerField(default=0)
    repo_pull_requests = models.IntegerField(default=0)
    repo_contributors = models.ManyToManyField(ContibutorModel, blank=None)
    repo_creation_date = models.DateTimeField()