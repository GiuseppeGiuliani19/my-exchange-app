"""exchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # registration
    path('register/', views.register, name="register"),
    path('', include('app.urls')),
    # url for login,i have used  crispy form that visulized in html page
    path('', include("django.contrib.auth.urls")),
    #bitcoins of users
    path('bitcoins_users', views.bitcoins_users, name="bitcoins_users"),
    #storic of transactions
    path('profit_or_loss_users', views.profit_or_loss_moneys, name='profit_or_loss'),
    path('profit_or_loss_crypto', views.profit_or_loss_crypto, name='profit_or_loss_bitcoins'),
    #wallet
    path('wallet', views.wallet, name='wallet'),
    #tutorial
    path('tutorial', views.tutorial, name='tutorial'),
    path('response_order_executed', views.response_order_executed, name='response_order_executed'),
    path('response_wallet_executed', views.response_wallet_executed, name='response_wallet_executed'),
  #  path('your_orders_executed', views.your_order_executed, name='your_orders_executed'),

]