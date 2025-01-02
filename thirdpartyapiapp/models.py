from django.db import models


class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField(null=True, blank=True)  # Allow null values
    description = models.CharField(max_length=255)
    retrieved_at = models.DateTimeField(auto_now_add=True)

class StockData(models.Model):
    symbol = models.CharField(max_length=10)
    price = models.FloatField()
    retrieved_at = models.DateTimeField(auto_now_add=True)