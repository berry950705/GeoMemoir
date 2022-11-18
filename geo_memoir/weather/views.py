from django.http import JsonResponse
from django.shortcuts import render
from weather.models import Weather


# Create your views here.
def weather_info(request, lang_code):
    city_list = ['Singapore', 'London', 'Taipei', 'Bangkok', 'Beijing', 'Seoul', 'Barcelona', 'Paris', 'Tokyo', 'Lima', 'Dubai', 'Seattle', 'Istanbul', 'Milan', 'Cairo', 'New York', 'Hong Kong', 'Denpasar', 'Toronto', 'Rio De Janeiro', 'Kuala Lumpur', 'Sydney', 'Cape Town']
    weather_data = Weather.objects.filter(city__in=city_list)
    data = {}
    for item in weather_data:
        data[item.city] = {'location': item.location, 'weather_info': item.weather_info,
                           'temperature': item.temperature,
                           'humidity': item.humidity, 'date': item.date, 'cur_time': item.cur_time}
    print(data)
    return JsonResponse({'code': 200, 'data': data})



