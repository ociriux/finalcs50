from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Food

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def food(request):
    foodItems = Food.objects.all().values()
    template = loader.get_template('food.html')
    context = {
        'foodItems' : foodItems,
    }
    return HttpResponse(template.render(context, request))