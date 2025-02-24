from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from usda_sync.models import Food, Nutrient, FoodSpec
import requests

def index(request):
    template = loader.get_template('index.html')
    context = {
        'user' : 'Chef',
    }
    return HttpResponse(template.render(context, request))

def food(request):
    foodItems = Food.objects.all().order_by('description')
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
