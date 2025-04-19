import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib import messages

# Load environment variables
load_dotenv()

def index(request):
    weather_data = None

    if request.method == "POST":
        city = request.POST.get("city")
        api_key = os.getenv("OPENWEATHER_API_KEY")          
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data.get("cod") != "404":
            utc_time = datetime.utcfromtimestamp(data["dt"])
            offset = data["timezone"]
            local_time = utc_time + timedelta(seconds=offset)

            weather_data = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
                "weather_condition": data["weather"][0]["main"],
                "local_time": local_time.strftime('%Y-%m-%d %H:%M:%S'),
            }
        else:
            messages.error(request, f"City '{city}' not found. Please try again.")

    return render(request, 'weather/index.html', {'weather': weather_data})

