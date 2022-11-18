from django.db import models

from story.models import Story
from user.models import UserProfile


# Create your models here.
class Gallery(models.Model):
    id = models.AutoField(primary_key = True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    created_name = models.DateTimeField(auto_now_add=True)
    updated_name = models.DateTimeField(auto_now=True)


