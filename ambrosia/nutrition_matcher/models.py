from django.db import models

class Food(models.Model):
    foodName = models.CharField(max_length=255)
    foodCategory = models.CharField(max_length=255)
    fatContent = models.IntegerField(null=True)
    sugarContent = models.IntegerField(null=True)
    proteinContent = models.IntegerField(null=True)
