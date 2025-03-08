from django.db.models import Sum, Count
from usda_sync.models import Food, Nutrient, FoodSpec

def find_top_matches(nutrient_ids):
    print("Starting matching Nutrients and Food...")
    top_foods = (
        Food.objects.filter(foodspec__nutrient__id__in=nutrient_ids)
        .annotate(
            total_score=Sum('foodspec__score'),
            nutrient_count=Count('foodspec__nutrient')
        )
        .annotate(average_score=1.0 * Sum('foodspec__score') / Count('foodspec__nutrient'))
        .order_by('-average_score')[:20]
    )
    return top_foods