import requests
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        if 'main' in r.keys():
            print("type----- ", type(r["main"]["temp"]))
            print("temp----- ", r["main"]["temp"])
            city_weather = {
                'city': city.name,
                'city_id': city.id,
                'temperature': r["main"]["temp"],
                'description': r["weather"][0]["description"],
                'icon': r["weather"][0]["icon"],
            }
            weather_data.append(city_weather)
        else:
            continue

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather.html', context)


def delete_city(request, pk):
    context = {}
    obj = get_object_or_404(City, id=pk)
    obj.delete()
    return redirect('home')
