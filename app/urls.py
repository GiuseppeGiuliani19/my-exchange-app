from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders, name='orders'),
    #orders executed
    path('orders_executed', views.orders_executed, name='orders_executed'),
    #link for new order
    path('order/new/', views.order_new, name='order_new'),
    path('wallet/new/', views.wallet_new, name='wallet_new'),
]