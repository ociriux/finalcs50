from django.contrib import admin
from .models import Food, Nutrient, FoodSpec, LastUpdate

class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'category',)

class NutrientAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'unit',)

class FoodSpecAdmin(admin.ModelAdmin):
    list_display = ('food', 'nutrient', 'amount',)

admin.site.register(Food, FoodAdmin)
admin.site.register(Nutrient, NutrientAdmin)
admin.site.register(FoodSpec, FoodSpecAdmin)
admin.site.register(LastUpdate)