from django.db import models

class FoodData(models.Model):
    fdc_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)
    # Weitere Felder entsprechend den USDA-Daten
