from django.urls import path

from gtoken import views

urlpatterns = [
    path('geo_login', views.tokens),
    path('google_login', views.google_token),

]

