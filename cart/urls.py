from django.urls import path
from .views import cart_add, cart_remove, cart_detail



app_name = 'cart'
urlpatterns = [
    path('', cart_detail, name='cart-detail'),
    path('add/<int:product_id>/', cart_add, name='cart-add'),
    path('remove/<int:product_id>/', cart_remove, name='cart-remove'),
]