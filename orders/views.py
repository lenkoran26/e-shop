from django.shortcuts import render
from .models import Order, OrderItem
from products.models import Products
from .forms import OrderForm

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

        # получаем корзину из сессии
        cart = request.session['cart']
        # получчаем номер только что созданного пустого заказа
        order_num = order_form.instance.number
        # получаем объект самого заказа из БД
        order = Order.objects.get(number = order_num)
        
        # проходимся по корзине и заносим товары в заказ
        for product_id in cart.keys():
            product = Products.objects.get(pk=product_id)
            quantity = cart[product_id]['quantity']
        
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            

    
