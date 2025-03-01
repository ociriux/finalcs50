from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from usda_sync.models import Food, Nutrient, FoodSpec
import requests

def index(request):
    nutrients = Nutrient.objects.all().order_by('description')
    template = loader.get_template('index.html')
    context = {
        'nutrients' : nutrients,
    }
    return HttpResponse(template.render(context, request))

def food(request):
    food = Food.objects.all().order_by('id')
    template = loader.get_template('food.html')
    context = {
        'food' : food,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    food = Food.objects.get(id=id)
    food_specs = FoodSpec.objects.filter(food_id=id).order_by('nutrient')
    template = loader.get_template('details.html')
    context = {
        'food_specs' : food_specs, 'food' : food,
    }
    return HttpResponse(template.render(context, request))
