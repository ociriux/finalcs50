from django.urls import path
from . import views

urlpatterns = [
    path('nutrition_matcher/', views.index, name='index'),
    path('food/', views.food, name='food'),
]