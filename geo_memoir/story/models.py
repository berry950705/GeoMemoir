from django.db import models
from user.models import UserProfile
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Story(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=128)
    area = models.CharField(max_length=32)
    category = models.CharField(max_length=32)
    country = models.CharField(max_length=64)
    photo = models.ImageField(upload_to='photo')
    photo_desc = models.CharField(max_length=512)
    content = models.TextField(default='')
    view = models.IntegerField(default=0)
    like = models.ManyToManyField(UserProfile, related_name='story_like')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=False)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='story_author')

    class Meta:
        db_table = 'story_story'
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'


class LikeStatus(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    is_clicked = models.BooleanField(default=False)

    class Meta:
        db_table = 'story_like_status'
        verbose_name = 'Like Status'
        verbose_name_plural = 'Like Status'


