from django.contrib import admin

from weather.models import Weather


# Register your models here.
class WeatherManager(admin.ModelAdmin):
    list_display = ['city', 'location', 'weather_icon', 'weather_info', 'temperature', 'visibility',
                    'humidity', 'dew_point', 'date', 'cur_time']


admin.site.register(Weather, WeatherManager)
