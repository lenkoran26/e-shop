
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView

from cart.models import CartUser
from cart.views import Cart, ProductCartUser
from products.models import Products

from .forms import OrderForm
from .models import Order, OrderItem

# удаление корзины пользователя из БД
def cart_delete(request, cart):
    # очищаем словарь
    cart.clear()
    #получаем объект корзины из БД
    cart_user = CartUser.objects.get(user=request.user)
    # удаляем его
    cart_user.delete()
    

# создание заказа
def create_order(request):
    # выдаем пустую форму для заполнения информации о заказе
    if request.method == 'GET':
        form = OrderForm()
        context = {'form': form}
        
        return render(request, template_name="orders/order.html", context=context)
    
    # создаем словарь из корзины если пользователь авторизован
    if request.user.id:
        cart = ProductCartUser(request).cart
    # либо если не авторизован
    else:
        cart = Cart(request).cart
    # если корзина пуста, заказ не создаем, переводим пользователя на главную страницу
    if len(cart) == 0:
        url = reverse('products:index')
        return redirect(url)
        
    # если нажата кнопка подтвердить заказ (метод POST)
    # получаем заполненную форму
    
    order_form = OrderForm(request.POST)
    
    # сохраняем форму заказа в БД
    if order_form.is_valid():
        order_form.save()
               
        # получаем номер только что созданного заказа
        order_num = order_form.instance.number
        # если пользователь авторизован, добавляем его в поле user заказа
        if request.user.id:
            user = User.objects.get(pk=request.user.id)
            order = Order.objects.get(number = order_num)
            order.user = user
        else:
            # иначе просто получаем объект самого заказа из БД
            order = Order.objects.get(number = order_num)
        
        total_price = 0
        
        # проходимся по корзине и заносим товары в заказ
        for product_id in cart.keys():
            # получаем товар из БД
            product = Products.objects.get(pk=product_id)
            # получаем количество товара из корзины
            quantity = cart[product_id]['quantity']
            # вычисляем стоимость 
            total_price += product.price * int(quantity)
            # создаем позицию товара в заказе в БД
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
        
        # сохраняем итоговую стоимость в заказе
        order.total_price = total_price
        order.save()
        
        # очищаем корзину после создания заказа
        if request.user.id:
            cart_delete(request, cart)
        else:
            cart.clear()
        
        context = {'order': order}
              
        return render(request, 'orders/order_success.html', context=context)
            
# вывод списка заказов пользователя
class OrdersListView(ListView):
    model = Order
    template_name = 'orders/user_orders.html'
    context_object_name = 'orders'
    
    # получаем заказы из БД по полю user 
    def get_queryset(self):
        # вызываем родительский метод
        super().get_queryset()
        # получаем пользователя
        user = self.request.user
        # фильтруем набор данных по пользователю
        queryset = Order.objects.filter(user=user)
        
        return queryset
        
# отображение информации о заказе
class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order-detail.html'
    context_object_name = 'order'


    
    
