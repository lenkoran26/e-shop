from django.urls import path
from .views import create_order, OrdersListView, OrderDetailView


app_name = 'orders'
urlpatterns = [
    path('', OrdersListView.as_view(), name='order-list'),
    path('new_order/', create_order, name='order-create'),
    path('order-info/<str:pk>/', OrderDetailView.as_view(), name='order-detail'),
]