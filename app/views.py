from django.shortcuts import render
from .models import Order, Wallet
from .forms import RegisterForm, OrderForm, WalletForm
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
from django.http import JsonResponse
from django.conf import settings


@login_required
def wallet_new(request):
        wallets = Wallet.objects.all()
        form = WalletForm()
        if request.method == "POST":
            form = WalletForm(request.POST)
            if form.is_valid():
                new_wallet = form.save()
                new_wallet.profile = request.user
                for wallet in wallets:
                    if wallet.profile == new_wallet.profile:
                           return render(request, 'app/error.html')
                else:
                           new_wallet.save()
                return redirect('wallet')
        else:
            form = WalletForm()
        contex = {'form': form}
        return render(request, 'app/wallet_new.html', contex)

def wallet(request):
    wallets = Wallet.objects.all()
    orders = Order.objects.all().filter(execute=True).order_by('-datetime')
    for wallet in wallets:
        for order in orders:
            if wallet.profile == order.profile and order.profit <= 0:
                wallet.wallet += order.profit
            elif wallet.profile == order.profile and order.profit >= 0:
                wallet.wallet += order.profit
    return render(request, 'app/wallet.html', {'wallets': wallets})

#method to do new order
@login_required
def order_new(request):
    wallets = Wallet.objects.all()
    form = OrderForm()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save()
            if request.method == "POST":
               if new_order.buy is True:
                    sell_Order = Order.objects.filter(sell=True, execute=False, price__lte=new_order.price).first()
                    if sell_Order != None:
                        profit_Bitcoin = new_order.quantity
                        profit_Buy = new_order.price
                        new_order.quantity = profit_Bitcoin
                        sell_Order.quantity = -profit_Bitcoin
                        new_order.profit = -profit_Buy
                        sell_Order.profit = profit_Buy
                        new_order.execute = True
                        sell_Order.execute = True
                        sell_Order.save()
                    else:
                        new_order.save()
               else:
                    buy_Order = Order.objects.filter(buy=True, execute=False, price__gte=new_order.price).first()
                    if buy_Order != None:
                        profit_Sell = buy_Order.price - new_order.price
                        new_order.profit = profit_Sell
                        new_order.execute = True
                        buy_Order.execute = True
                        buy_Order.save()
                    else:
                         new_order.save()
               new_order.profile = request.user
               new_order.save()
               return redirect('orders')
    else:
              form = OrderForm()
    contex = {'form': form}
    return render(request, 'app/order_new.html', contex)

def orders(request):
    orders = Order.objects.all().order_by('-datetime').filter(execute=False)
    return render(request, 'app/orders.html', {'orders': orders})

def orders_executed(request):
    orders_executed = Order.objects.all().filter(execute=True).order_by('-datetime')
    return render(request, 'app/orders_executed.html', {'orders_executed': orders_executed})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
        return redirect("/login")
    else:
        form = RegisterForm()
    return render(request, "app/register.html", {"form": form})

def bitcoins_users(request):
    random.seed(999)
    users = User.objects.all()
    response = []
    for user in users:
        response.append(
            {
               'username': user.username,
               'bitcoins': random.randint(1, 10)
            }

        )

    return JsonResponse(response, safe=False)

def profit_or_loss_moneys(request):
    orders = Order.objects.all().filter(execute=True).order_by('-datetime')
    users = User.objects.all()
    response = []
    for user in users:
        for order in orders:
            if user.username == order.profile.username:
                     response.append(
                         {
                              user.username:  order.profit,
                              'datetime': order.datetime,
                         }
                     )

    return JsonResponse(response, safe=False)


def profit_or_loss_bitcoins(request):
    orders = Order.objects.all().filter(execute=True).order_by('-datetime')
    users = User.objects.all()
    response = []
    for user in users:
        for order in orders:
            if user.username == order.profile.username:
                     response.append(
                         {
                              user.username:  order.quantity,
                             'datetime': order.datetime,
                         }
                     )
    return JsonResponse(response, safe=False)

# def balance(request):
#     orders = Order.objects.all().filter(execute=True).order_by('-datetime')
#     users = User.objects.all()
#     balance = 0
#     response = []
#     for user in users:
#         for order in orders:
#             if user.username == order.profile.username:
#                      # balance -= order.profit
#                      balance += order.profit
#                      # balance.append(order.profit)
#                      # all_balance = sum(balance)
#                      response.append(
#                          {
#                               user.username:  balance,
#                          }
#                      )
#
#     return JsonResponse(response, safe=False)

