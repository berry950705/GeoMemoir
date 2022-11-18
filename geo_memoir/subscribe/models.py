from django.db import models


# Create your models here.
class Subscribe(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=32)
    email = models.EmailField()
    created_time = models.DateTimeField(auto_now_add=True)

