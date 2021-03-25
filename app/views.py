from django.shortcuts import render, get_object_or_404
from .models import Order, Wallet
from .forms import RegisterForm, OrderForm, WalletForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random
from django.http import JsonResponse
from django.utils import timezone
import json
from django.http import HttpResponse

#this function is used to represent the newly created wallet
def response_wallet_executed(request):
    wallets = list(Wallet.objects.all())
    last_wallet = wallets[-1]
    return render(request, 'app/response_wallet_executed.html', {'last_wallet': last_wallet})
#this function is used to represent the newly created order
def response_order_executed(request):
    orders = list(Order.objects.all())
    last_order = orders[-1]
    return render(request, 'app/response_order_executed.html', {'last_order': last_order})

def tutorial(request):
    return render(request, 'app/Tutorial.html')
@login_required
def wallet_new(request):
        wallets = Wallet.objects.all()
        form = WalletForm()
        if request.method == "POST":
            form = WalletForm(request.POST)
            form.profile = request.user
            for wallet in wallets:
                if form.profile == wallet.profile:
                    return render(request, 'app/error.html')
            if form.is_valid():
                        form.save()
            return redirect('response_wallet_executed')
        else:
            form = WalletForm()
        contex = {'form': form}
        return render(request, 'app/wallet_new.html', contex)
#update the balance of wallet
def wallet(request):
       wallets = Wallet.objects.all()
       orders = Order.objects.all().filter(order_close=True, add_to_Wallet=False)
       for wallet in wallets:
            for order in orders:
                if wallet.profile == order.profile and order.profit <= 0 and order.add_to_Wallet == False:
                                wallet.budget += order.profit
                                order.add_to_Wallet = True
                                order.save()
                                wallet.save()

                elif wallet.profile == order.profile and order.profit > 0 and order.add_to_Wallet == False:
                                wallet.budget += order.profit
                                order.add_to_Wallet = True
                                order.save()
                                wallet.save()

       return render(request, 'app/wallet.html', {'wallets': wallets})

#method to do new order
@login_required
def order_new(request):
    orders = Order.objects.all()
    wallets = Wallet.objects.all()
    form = OrderForm()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save()
            for wallet in wallets:
                for order in orders:
                   if new_order.choice == ('buy') and new_order.price <= wallet.budget and \
                           new_order.prenotation == 'False':
                            sell_Order = Order.objects.filter(prenotation='False', choice='sell', order_close=False,
                                                              price__lte=new_order.price,
                                                              choise_crypto=new_order.choise_crypto).first()
                            if sell_Order != None:
                                profit_Bitcoin = new_order.quantity
                                profit_Buy = new_order.price
                                new_order.quantity = profit_Bitcoin
                                sell_Order.quantity = -profit_Bitcoin
                                new_order.profit = -profit_Buy
                                sell_Order.profit = profit_Buy
                                new_order.order_close = True
                                sell_Order.order_close = True
                                sell_Order.date_executed = timezone.now()
                                sell_Order.save()
                            else:
                                new_order.save()
                   elif new_order.choice == ('buy') and new_order.price <= wallet.budget\
                       and new_order.prenotation != 'False':
                       sell_Order = Order.objects.filter(prenotation=new_order.profile, choice='sell',
                                                         order_close=False,
                                                         price__lte=new_order.price,
                                                         choise_crypto=new_order.choise_crypto).first()
                     #  for order in sell_Order:
                       if sell_Order != None and new_order.prenotation == str(sell_Order.profile):
                                   profit_Bitcoin = new_order.quantity
                                   profit_Buy = new_order.price
                                   new_order.quantity = profit_Bitcoin
                                   sell_Order.quantity = -profit_Bitcoin
                                   new_order.profit = -profit_Buy
                                   sell_Order.profit = profit_Buy
                                   new_order.order_close = True
                                   sell_Order.order_close = True
                                   sell_Order.save()
                       else:
                                   new_order.save()

                   elif new_order.choice == ('buy') and new_order.price > wallet.budget:
                       new_order.delete()
                       return render(request, 'app/error_order.html')
                   elif new_order.choice == ('sell')   and new_order.prenotation != 'False':
                            buy_Order = Order.objects.filter(prenotation=str(new_order.profile), choice='buy',
                                                             order_close=False,
                                                             price__gte=new_order.price,
                                                             choise_crypto=new_order.choise_crypto).first()
                           # for order in buy_Order:
                            if buy_Order != None and new_order.prenotation == str(buy_Order.profile):
                                        profit_Sell = buy_Order.price
                                        new_order.quantity = -new_order.quantity
                                        new_order.profit = profit_Sell
                                        new_order.order_close = True
                                        buy_Order.date_executed = timezone.now()
                                        buy_Order.order_close = True
                                        buy_Order.profit = -buy_Order.price
                                        buy_Order.save()
                            else:
                                         new_order.save()
                   elif new_order.choice == ('sell')   and new_order.prenotation == 'False':
                            buy_Order = Order.objects.filter(prenotation='False', choice='buy', order_close=False,
                                                             price__gte=new_order.price,
                                                             choise_crypto=new_order.choise_crypto).first()
                            if buy_Order != None:
                                profit_Sell = buy_Order.price
                                new_order.quantity = -new_order.quantity
                                new_order.profit = profit_Sell
                                new_order.order_close = True
                                buy_Order.date_executed = timezone.now()
                                buy_Order.order_close = True
                                buy_Order.profit = -buy_Order.price
                                buy_Order.save()
                            else:
                                 new_order.save()
                   new_order.profile = request.user
                   new_order.save()
                   return redirect('response_order_executed')

    else:
              form = OrderForm()
    contex = {'form': form}
    return render(request, 'app/order_new.html', contex)

def orders(request):
    orders = Order.objects.all().order_by('-datetime').filter(order_close=False)
    return render(request, 'app/orders.html', {'orders': orders})

def orders_executed(request):
    orders_executed = Order.objects.all().filter(order_close=True).order_by('-datetime')
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
    orders = Order.objects.all().filter(order_close=True).order_by('-datetime')
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


    return HttpResponse(response, content_type="text/plain")
    #return json.dumps(response, indent=4, sort_keys=True, default=str)

def profit_or_loss_crypto(request):
    orders = Order.objects.all().filter(order_close=True).order_by('-datetime')
    users = User.objects.all()
    response = []
    for user in users:
        for order in orders:
            if user.username == order.profile.username:
                     response.append(
                         {
                              user.username:  order.quantity,
                             'crypto': order.choise_crypto,
                             'datetime': order.datetime,
                         }
                     )
   # return JsonResponse(response, safe=False)
    return HttpResponse(response, content_type="text/plain")

# def your_order_executed(request):
#    # orders = Order.objects.filter
#     wallets = Wallet.objects.all()
#     users = User.objects.all()
#     orders = Order.objects.all()
#     for wallet in wallets:
#     #for order in orders:
#          for user in users:
#                  #  orders = Order.objects.filter(profile=user.id)
#             #if user. == order.profile:
#                    for order in orders:
#                              your_order = Order.objects.filter(profile=wallet.profile)
#                              return render(request, "app/your_order_executed.html", {"your_order": your_order})




