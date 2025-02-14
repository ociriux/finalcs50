from django.contrib import admin
from .models import Food

class FoodAdmin(admin.ModelAdmin):
    list_display = ("foodName", "foodCategory", "id",)

admin.site.register(Food, FoodAdmin)