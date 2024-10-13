from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    password = models.CharField(max_length=128, editable=False)
    name = models.CharField(max_length=150, default="", editable=True)
    avatar = models.URLField(blank=True)

    def tweets_count(self):
        return self.tweets.count()

    def __str__(self):
        if self.name:
            return f"{self.username} ({self.name})"
        else:
            return self.username
