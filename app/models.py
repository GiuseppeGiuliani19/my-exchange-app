from django.db import models
from djongo.models.fields import ObjectIdField
from django.contrib.auth.models import User
from django.conf import settings

class Wallet(models.Model):
    _id = ObjectIdField()
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    budget = models.FloatField()

class Order(models.Model):
    _id = ObjectIdField()
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    quantity = models.FloatField()
    BUY_SELL_CHOICES = (
        ('buy', 'Buy'),
        ('sell', 'Sell')
    )
    #this parameter indicates  the user's choice : buy or sell
    choice = models.CharField(max_length=10, choices=BUY_SELL_CHOICES)
    #this parameter is used if someone wants to make private orders
    prenotation = models.CharField(max_length=30, default=False)
    #this parameter indicates that order is open or not,if it is open the parameter equal false
    order_close = models.BooleanField(blank=True, default=False)
    date_executed = models.DateTimeField(auto_now_add=True)
    profit = models.FloatField(default=0)
    #this parameter is used to add the closed order in the wallet
    add_to_Wallet = models.BooleanField(blank=True, default=False)

