
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView

from cart.models import CartUser
from cart.views import Cart, ProductCartUser
from products.models import Products

from .forms import OrderForm
from .models import Order, OrderItem


def cart_delete(request, cart):
    cart.clear()
    cart_user = CartUser.objects.get(user=request.user)
    cart_user.delete()
    

# создание заказа
def create_order(request):
    # выдаем пустую форму для заполнения информации о заказе
    if request.method == 'GET':
        form = OrderForm()
        context = {'form': form}
        
        return render(request, template_name="orders/order.html", context=context)
    
    # если нажата кнопка подтвердить заказ
    # получаем заполненную форму
    order_form = OrderForm(request.POST)
    
    # сохраняем пустой заказ в БД
    if order_form.is_valid():
        order_form.save()

        # получаем корзину из БД
        if request.user.id:
            cart = ProductCartUser(request).cart
        # либо получаем корзину из сессии
        else:
            cart = Cart(request)
        
        # получчаем номер только что созданного пустого заказа
        order_num = order_form.instance.number
        user = User.objects.get(pk=request.user.id)
        # получаем объект самого заказа из БД
        order = Order.objects.get(number = order_num)
        order.user = user
        total_price = 0
        
        # проходимся по корзине и заносим товары в заказ
        for product_id in cart.keys():
            product = Products.objects.get(pk=product_id)
            quantity = cart[product_id]['quantity']
            total_price += product.price * int(quantity)
            # создаем позицию товара в заказе
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
        
        order.total_price = total_price
        order.save()
        
        if request.user.id:
            cart_delete(request, cart)
        else:
            cart.clear()
        
        context = {'order': order}
        
        return render(request, 'orders/order_success.html', context=context)
            

class OrdersListView(ListView):
    model = Order
    template_name = 'orders/user_orders.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        super().get_queryset()
        user = self.request.user
        queryset = Order.objects.filter(Q(email = user.email) | Q(user=user))
        
        return queryset
    
    
