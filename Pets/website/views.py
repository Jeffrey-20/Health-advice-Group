from turtle import speed
from django.shortcuts import render
from datetime import datetime


# Create your views here.
import time
import requests
from django.shortcuts import render
from django.contrib import messages


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignUpForm
from django.contrib.auth import login as auth_login



import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import WeatherImpact


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





def register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def login_view(request): # Renamed to avoid conflict with auth_login
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, 'Logged in successfully!')
            
            # Check for '?next=' parameter, otherwise go to 'dashboard'
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home') 




@login_required
def dashboard_view(request):
    api_key = '505789d4dff3f9eda7a56f94acd3b1b0'
    city = request.GET.get('city')

    # 1. Handle "POST" request (Saving a new Impact Log)
    if request.method == 'POST':
        WeatherImpact.objects.create(
            user=request.user,
            city=request.POST.get('city'),
            temperature=request.POST.get('temperature'),
            condition=request.POST.get('condition'),
            impact_note=request.POST.get('impact_note')
        )
        messages.success(request, "Impact log saved successfully!")
        return redirect('dashboard')

    # 2. Weather API Logic
    if not city or city.strip() == "":
        city = 'Worksop'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    weather_data = None

    if response.status_code == 200:
        data = response.json()
        main_weather = data['weather'][0]['main']
        
        # Day/Night logic
        current_time = data['dt']
        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        is_night = current_time < sunrise or current_time > sunset
        
        mapping = {
            'Clear': 'clear', 'Clouds': 'clouds', 'Rain': 'rain',
            'Drizzle': 'rain', 'Thunderstorm': 'rain', 'Snow': 'snow',
            'Mist': 'clouds', 'Fog': 'clouds',
        }

        condition = mapping.get(main_weather, 'clear')
        time_prefix = "night_" if is_night else "day_"

        weather_data = {
            'city': data['name'],
            'main': main_weather,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'icon': data['weather'][0]['icon'],
            'bg_image': f"{time_prefix}{condition}.jpg"
        }
    else:
        messages.error(request, f"Could not find weather for '{city}'. Showing default.")

    # 3. Fetch History (Only for the logged-in user)
   
    history = WeatherImpact.objects.filter(user=request.user).order_by('-created_at')

# FORCE DEBUG PRINT
    print("--- DEBUGGING HISTORY ---")
    print(f"Current User: {request.user}")
    print(f"Query: {history.query}") # This shows the actual SQL being run
    print(f"Count: {len(history)}") # Using len() forces the database to answer
    for h in history:
        print(f"Note found: {h.impact_note}")
    print("-------------------------")


    context = {
        'weather': weather_data,
        'history': history
    }

    return render(request, 'dashboard.html', context)



# 4. Auxiliary functions for Delete and Download
@login_required
def delete_impact(request, pk):
    log = get_object_or_404(WeatherImpact, pk=pk, user=request.user)
    log.delete()
    return redirect('dashboard')

@login_required
def download_impacts(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="weather_impacts.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'City', 'Temp', 'Condition', 'Note'])
    
    logs = WeatherImpact.objects.filter(user=request.user)
    for log in logs:
        writer.writerow([log.created_at, log.city, log.temperature, log.condition, log.impact_note])
        
    return response