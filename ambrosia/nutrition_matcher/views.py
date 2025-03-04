from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from usda_sync.models import Food, Nutrient, FoodSpec
from . import matcher
import requests

def index(request):
    nutrients = Nutrient.objects.all().order_by('description')
    template = loader.get_template('index.html')
    context = {
        'nutrients' : nutrients,
    }
    return HttpResponse(template.render(context, request))

def nutrition_matcher(request):
    if request.method == "POST":
        target_nutrient_ids = request.POST.getlist("nutrient_target")
        target_nutrient_ids = [int(x) for x in target_nutrient_ids]
        matched_food = matcher.find_top_matches(target_nutrient_ids)
        context = {
            'matched_food' : matched_food, 'target_nutrient_ids' : target_nutrient_ids
        }
        return render(request, "matched.html", context)
    return HttpResponse("Invalid request", status=400)

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
