from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Food
import requests

def index(request):
    template = loader.get_template('index.html')
    context = {
        'user' : 'Chef',
    }
    return HttpResponse(template.render(context, request))

def food(request):
    foodItems = Food.objects.all().order_by('foodName')
    template = loader.get_template('food.html')
    context = {
        'food' : foodItems,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    foodItem = Food.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'food' : foodItem,
    }
    return HttpResponse(template.render(context, request))



##########################
def get_food_data(query):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "api_key": "gdeU5YEXk67OSPqgivqM1SU4ltoiozPa5tsADXfJ",
        "query": query,
        "pageSize": 25
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        # Fehlerbehandlung je nach Bedarf
        return None
####################################

def usda(request):
    template = loader.get_template('usda.html')
    query = request.GET.get("query", "protein")  # Beispiel: Default-Suche "ketogen"
    data = get_food_data(query)
    context = {
        'data' : data,
    }
    return render(request, "usda.html", context)
