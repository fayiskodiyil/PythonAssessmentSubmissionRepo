import uuid
from io import BytesIO
import requests

from django.db import models
from django.core.files.base import ContentFile
from django.core.files import File


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "topics"

    def __str__(self):
        return self.name
    

class Repository(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    avatar_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    stars = models.IntegerField(default=0)
    forks = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    topic = models.ManyToManyField(Topic)
    html_url = models.URLField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "repositories"
        ordering = ["-date_added"]

    def __str__(self):
        return self.name
