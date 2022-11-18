from django.urls import path
from weather import views


urlpatterns = [
    path('info', views.weather_info),


]