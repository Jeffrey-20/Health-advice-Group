from turtle import speed
from django.shortcuts import render
from datetime import datetime


# Create your views here.
import time
import requests
from django.shortcuts import render
from django.contrib import messages


from django.shortcuts import render, redirect




def home(request):
    api_key = '505789d4dff3f9eda7a56f94acd3b1b0'
    # Default to Worksop if the search bar is empty
    city = request.GET.get('city')


    if not city or city.strip() == "":
        city = 'Worksop'


    weather_data = None


    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
   
    if response.status_code == 200:
        data = response.json()
        main_weather = data['weather'][0]['main']
       
        # Check if it's night using the API's sunrise/sunset timestamps
        current_time = data['dt']
        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        is_night = current_time < sunrise or current_time > sunset
       
        # Map API conditions to your filenames
        # Format: API_CONDITION : FILENAME_PART
        mapping = {
            'Clear': 'clear',
            'Clouds': 'clouds',
            'Rain': 'rain',
            'Drizzle': 'rain',
            'Thunderstorm': 'rain', # Or 'storm' if you have a separate image
            'Snow': 'snow',
            'Mist': 'clouds',
            'Fog': 'clouds',
        }


        # Get the filename part, default to 'clear' if condition is unknown
        condition = mapping.get(main_weather, 'clear')
        time_prefix = "night_" if is_night else "day_"


        weather_data = {
           
            'city': data['name'],
            'main': data['weather'][0]['main'], # This is what we use for the background
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'icon': data['weather'][0]['icon'],
            'bg_image': f"{time_prefix}{condition}.jpg"
        }
   
    return render(request, 'index.html', {'weather': weather_data})


# views.py




def forecast(request):
    api_key = '505789d4dff3f9eda7a56f94acd3b1b0'
    city = request.GET.get('city')


    if not city:
        return redirect('home')  # Go back home if no city provided


    # Using the 5-day / 3-hour forecast API
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
   
    forecast_list = []
    if response.status_code == 200:
        data = response.json()
        # The API returns 40 intervals (8 per day).
        # We filter to show one per day (every 8th item).
        for item in data['list'][::8]:
            date_obj = datetime.strptime(item['dt_txt'], "%Y-%m-%d %H:%M:%S")


            forecast_list.append({
                'day_time': date_obj.strftime("%A "),  # Monday (12:00)
                'date': date_obj.strftime("%d %b %Y"),        # 12 Feb 2026
                'temp': item['main']['temp'],
                'humidity': item['main']['humidity'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon'],
            })


   
    return render(request, 'forecast.html', {'forecast': forecast_list, 'city': city})






def dashboard(request):
    return render(request, 'dashboard.html')




