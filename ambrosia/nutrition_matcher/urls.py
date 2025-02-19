from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('food/', views.food, name='food'),
    path('food/details/<int:id>', views.details, name='details'),
    path('usda/', views.usda, name='usda'),
]