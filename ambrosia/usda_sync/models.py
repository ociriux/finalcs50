from django.db import models

class Food(models.Model):
        food_id = models.IntegerField(primary_key=True)
        description = models.CharField(max_length=255)

class Nutrient(models.Model):
        nutrient_id = models.IntegerField(primary_key=True)