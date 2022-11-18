from django.db import models
import random


# Create your models here.
def default_motto():
    signs = ['Weaknesses are just strengths in the wrong environment.',
             'Try to be a rainbow in someone’s cloud.',
             'Definitions belong to the definers, not the defined.',
             'The power of imagination makes us infinite.',
             'The secret of getting ahead is getting started.',
             ]
    return random.choice(signs)


class UserProfile(models.Model):
    id = models.AutoField(primary_key = True)
    google_id = models.CharField(max_length=100, unique=True, null=True)
    google_pic = models.CharField(max_length=255, null=True)
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128, null=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatar', default='avatar/avatar.png')
    background_img = models.ImageField(upload_to='background', null=True)
    profile_name = models.CharField(max_length=128, default="My Profile Name")
    motto = models.CharField(max_length=128, default=default_motto)
    self_intro = models.TextField(default='')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_user_profile'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

