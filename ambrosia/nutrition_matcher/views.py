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


def usda(request):
    api_key = 'gdeU5YEXk67OSPqgivqM1SU4ltoiozPa5tsADXfJ'
    query = request.GET.get('query', 'apple')  # Standardabfrage 'apple', falls keine Abfrage gestellt wird
    url = 'https://api.nal.usda.gov/fdc/v1/foods/search'
    params = {
        'api_key': api_key,
        'query': query,
        'pageSize': 10  # Anzahl der zurückgegebenen Ergebnisse
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        foods = data.get('foods', [])
    else:
        foods = []
    return render(request, 'usda.html', {'foods': foods, 'query': query})
