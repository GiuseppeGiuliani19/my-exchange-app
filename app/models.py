from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Wallet(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.FloatField()

class Order(models.Model):
    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    quantity = models.FloatField()
    BUY_SELL_CHOICES = (
        ('buy', 'Buy'),
        ('sell', 'Sell')
    )
    choice = models.CharField(max_length=10, choices=BUY_SELL_CHOICES)
    prenotation = models.CharField(max_length=30, default=False)
    execute = models.BooleanField(blank=True, default=False)
    date_executed = models.DateTimeField(auto_now_add=True)
    profit = models.FloatField(default=0)
    add_to_Wallet = models.BooleanField(blank=True, default=False)

