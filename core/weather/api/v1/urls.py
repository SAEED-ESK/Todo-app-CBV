from django.urls import path
from .views import WeatherAPI

urlpatterns = [
    path('weather-api/<str:city>', WeatherAPI.as_view(), name='weather_api'),
]