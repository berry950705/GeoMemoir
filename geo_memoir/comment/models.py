from django.db import models
from user.models import UserProfile
from story.models import Story

# Create your models here.


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=512)
    parent_comment = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    commenter = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

