from django.db.models import Sum
from usda_sync.models import Food, Nutrient, FoodSpec

def find_top_matches(nutrient_ids):
    print("Starting matching Nutrients and Food...")
    top_foods = (
        Food.objects.filter(foodspec__nutrient__id__in=nutrient_ids)
        .annotate(total_score=Sum('foodspec__score'))
        .order_by('-total_score')  # absteigend sortieren, d.h. höchste Summe zuerst
        [:20]  # maximal 10 Ergebnisse
    )
    print(top_foods)
    return top_foods