from django.db import models

# Create your models here.


class Weather(models.Model):
    id = models.AutoField(primary_key = True)
    city = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    weather_icon = models.CharField(max_length=80)
    weather_info = models.CharField(max_length=64)
    temperature = models.CharField(max_length=16)
    visibility = models.CharField(max_length=16)
    humidity = models.CharField(max_length=16)
    dew_point = models.CharField(max_length=16)
    date = models.CharField(max_length=16)
    cur_time = models.TimeField()

    class Meta:
        verbose_name_plural = 'Weather'






