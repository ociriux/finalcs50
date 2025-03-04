from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nutrition_matcher/', views.nutrition_matcher, name='nutrition_matcher'),
    path('food/', views.food, name='food'),
    path('food/details/<int:id>', views.details, name='details'),
]