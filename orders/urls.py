from django.urls import path
from .views import create_order, OrdersListView


app_name = 'orders'
urlpatterns = [
    path('new_order/', create_order, name='order-create'),
    path('orders/', OrdersListView.as_view(), name='order-list'),
]