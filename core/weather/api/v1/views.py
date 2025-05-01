# weather/views.py
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
import requests

class WeatherAPI(APIView):
    @method_decorator(cache_page(60 * 20))
    def get(self, request, city):
        api_key = 'd045153a34cb3712b3771ae71cf070a9'

        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url)
        print(response)
        if response.status_code == 200:
            data = response.json()
        else:
            return JsonResponse({'error': 'Failed to fetch weather'}, status=500)

        return JsonResponse({
            'city': city,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        })
