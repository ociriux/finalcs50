from django.db import models

class Food(models.Model):
        id = models.IntegerField(primary_key=True)
        description = models.CharField(max_length=255)
        category = models.CharField(max_length=255)
        calorie_conversion_factor_protein = models.FloatField(null=True)
        calorie_conversion_factor_fat = models.FloatField(null=True)
        calorie_conversion_factor_carbs = models.FloatField(null=True)

        def __str__(self):
                return f"{self.id} - {self.description}"

class Nutrient(models.Model):
        id = models.IntegerField(primary_key=True)
        description = models.CharField(max_length=255)
        unit = models.CharField(max_length=255)

        def __str__(self):
                return self.description
        
class FoodSpec(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    score = models.FloatField(default=0)

    class Meta:
        unique_together = ('food', 'nutrient')

    def __str__(self):
        return f"{self.food} - {self.nutrient}: {self.amount} {self.nutrient.unit}"
    
class LastUpdate(models.Model):
    url = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return self.url