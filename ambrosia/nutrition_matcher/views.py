from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from usda_sync.models import Food, Nutrient, FoodSpec
from . import matcher
import requests

def index(request):
    template = loader.get_template('index.html')
    foods = Food.objects.all().order_by('description')
    nutrients = Nutrient.objects.all().order_by('description')
    foodspecs = FoodSpec.objects.all()
    context = {
        'foods' : foods, 'nutrients' : nutrients, 'foodspecs' : foodspecs,
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

def build_label(request):
    if request.method == "POST":
        selected = request.POST.getlist("id")
        foodspecs = FoodSpec.objects.filter(selected=id)
        context = {
            'foodspecs' : foodspecs,
        }
        return render(request, "label.html", context)
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
    foodspecs = FoodSpec.objects.filter(food_id=id).order_by('nutrient')
    template = loader.get_template('details.html')
    context = {
        'foodspecs' : foodspecs, 'food' : food,
    }
    return HttpResponse(template.render(context, request))
