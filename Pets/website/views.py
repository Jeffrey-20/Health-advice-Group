from django.shortcuts import render

# Create your views here.

import requests
from django.shortcuts import render
from django.contrib import messages

def home(request):
    # Your API Key
    api_key = '505789d4dff3f9eda7a56f94acd3b1b0'
    weather_data = None
    city = request.GET.get('city') # Get city from search bar

    if city:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
            }
        else:
            messages.error(request, f"City '{city}' not found. Please try again.")

    return render(request, 'index.html', {'weather': weather_data})