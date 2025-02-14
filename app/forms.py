from django import forms
from .models import Order, Wallet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ('fiat_budget', 'btc_budget', 'eth_budget', 'dot_budget', 'ada_budget')
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('price', 'quantity', 'choice', 'choise_crypto', 'prenotation')

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]