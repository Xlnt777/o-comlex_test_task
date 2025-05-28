import requests, json
from django.shortcuts import render, redirect
from .forms import CityForm
from .models import SearchHistory, CitySearch
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from django.urls import reverse



def get_coordinates(city_name):
    response = requests.get("https://geocoding-api.open-meteo.com/v1/search", params={
        "name": city_name,
        "count": 1,
        "language": "ru",
        "format": "json"
    })
    data = response.json()
    if data.get("results"):
        result = data["results"][0]
        return result["latitude"], result["longitude"], result["name"]
    return None, None, None

def get_weather(latitude, longitude):
    response = requests.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "hourly": "relative_humidity_2m,surface_pressure",
        "timezone": "Europe/Moscow"
    })

    data = response.json()
    weather = data.get("current_weather", {})
    current_time = weather.get("time")

    if not current_time:
        return weather
    
    try:
        current_dt = datetime.fromisoformat(current_time)
        times = [datetime.fromisoformat(t) for t in data["hourly"]["time"]]

        closest_index = min(range(len(times)), key=lambda i: abs(times[i] - current_dt))

        weather["humidity"] = data["hourly"]["relative_humidity_2m"][closest_index]
        weather["pressure"] = data["hourly"]["surface_pressure"][closest_index]
    except Exception as e:
        weather["humidity"] = weather["pressure"] = None
        print("Ошибка при извлечении расширенных данных:", e)

    return weather

def home(request):
    weather_data = None
    city_name = None
    error = None

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            input_name = form.cleaned_data['city'].strip().title()
            lat, lon, resolved_name = get_coordinates(input_name)

            if lat and lon:
                city_name = resolved_name
                weather_data = get_weather(lat, lon)

                request.session['last_city'] = resolved_name
                request.session['weather_data'] = weather_data
                return redirect('home')

            else:
                request.session['error'] = "Город не найден."
                return redirect('home')
    else:
        form = CityForm()
        city_name = request.session.get('last_city')
        weather_data = request.session.pop('weather_data', None)
        error = request.session.pop('error', None)

    return render(request, 'weather/index.html', {
        'form': form,
        'weather': weather_data,
        'city': city_name,
        'error': error,
        'last_city': city_name,
    })

def autocomplete_city(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse([], safe=False)

    response = requests.get("https://geocoding-api.open-meteo.com/v1/search", params={
        "name": query,
        "count": 5,
        "language": "ru",
        "format": "json"
    })

    suggestions = []
    data = response.json()
    if "results" in data:
        suggestions = [item["name"] for item in data["results"]]

    return JsonResponse(suggestions, safe=False)



def city_stats_api(request):
    data = list(CitySearch.objects.values('name', 'count').order_by('-count'))
    json_data = json.dumps(data, ensure_ascii=False, indent=2)
    return HttpResponse(json_data, content_type='application/json')



