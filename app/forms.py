from django import forms
from .models import Order, Wallet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ('profile', 'wallet')
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('profile', 'price', 'quantity', 'buy', 'sell', 'execute', 'profit')

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]