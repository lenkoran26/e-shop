import json
from market import settings
from products.models import Products
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Products
from .forms import CartAddProductForm
from cart.models import CartUser, CartItem
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse


# Create your views here.

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.user = request.user
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart


    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()


    def save(self):
        self.session.modified = True
    

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Products.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
      
   
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())  
    

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()


@require_POST
def cart_add(request, product_id):
    if request.user.id:
        return add_cart_db(request, product_id)
    
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    form = CartAddProductForm(request.POST)
    
        
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, 
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    else:
        # добавляем  1 единицу товара
        cart.add(product=product, 
                 quantity=1,
                 override_quantity=False)
    
    # переходим на страницу корзины
    return redirect('cart:cart-detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product)
    
    return redirect('cart:cart-detail')


def cart_detail(request):
    if request.user.id:
        cart = ProductCartUser(request)
    else:
        cart = Cart(request)
        
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    return render(request, 'cart/cart-detail.html', {'cart': cart})



# корзина для авторизованного пользователя (хранится постоянно  в БД)
class ProductCartUser:
    # инициализация корзины
    def __init__(self, request):
        # создаем объект словаря для хранения товаров
        self.cart = {}
        # получаем текущего пользователя, чтобы знать, с чьей корзиной работать
        self.user = request.user
        # получаем корзину пользователя из БД или создаем пустую (если нет корзины)
        self.user_cart, created = CartUser.objects.get_or_create(user=self.user)
        # получаем позиции товаров в корзине
        products_in_cart = CartItem.objects.filter(cart=self.user_cart)
        """ заполняем корзину (словарь) элементами из корзины (БД) 
        {
        "1": 
          {
           "quantity": "2",
           "price": "35000.00"
          },
          "2": 
          {
           "quantity": "3",
           "price": "40000.00"
          },
        }
        """
        for item in products_in_cart:
            self.cart[str(item.product_id)] = {'quantity': str(item.quantity), 'price': str(item.product.price)}

    # метод добавления товара в корзину (словарь)
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        #product = Products.objects.get(pk=product.id)
        
        # проверяем наличие товара в корзине, если нет, то добавляем товар
        if product_id not in self.cart:
            self.cart[product_id]={'quantity': str(quantity), 'price': str(product.price)}
        # иначе - обновляем количество
        else:
            # если не нужно перезаписать количество
            if not override_quantity:
                # увеличиваем количество товара на необходимое
                current_quantity = int(self.cart[product_id]['quantity'])
                self.cart[product_id]['quantity'] = str(current_quantity+quantity)
            # иначе - перезаписываем
            else:
                self.cart[product_id]['quantity'] = quantity
        # вызываем метод сохранения в БД
        self.save()

    # метод сохранения в БД
    def save(self):
        # получаем каждый продукт по его ИД в словаре
        for id in self.cart:
            product = Products.objects.get(pk=int(id))
            # проверяем наличие товара в корзине БД
            # если есть - обновляем количество товара            
            if CartItem.objects.filter(cart=self.user_cart, product=product).exists():
                item = CartItem.objects.get(cart=self.user_cart, product=product)
                item.quantity = self.cart[id]['quantity']
                item.save()
            # иначе - создаем новую позицию товара в корзине
            else:
                CartItem.objects.create(cart=self.user_cart, product=product, quantity=self.cart[id]['quantity'])
    
    
    def remove(self, product_id, request):
        product = Products.objects.get(pk=product_id)
        cart_user = CartUser.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart_user, product=product)
        cart_item.delete()


    # метод подсчета товаров в корзине
    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())
    

    # создание итератора для элементов корзины (чтобы можно было проходиться по элементам в цикле)
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Products.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        # добавление в словарь корзины объекта товара с ключом "product"
        for product in products:
            cart[str(product.id)]['product'] = product
        # добавление в словарь корзины стоимости позиции товара с учетом количества
        for item in cart.values():
            item['total_price'] = item['product'].price * int(item['quantity'])
            yield item
    

    # метод подсчета общей стоимости товаров в корзине
    def get_total_price(self):
        return sum(Decimal(item['price']) * int(item['quantity']) for item in self.cart.values())


# добавление товара в корзину методом POST
@require_POST
def add_cart_db(request, product_id):
    # получаем объект корзины
    cart = ProductCartUser(request)
    # получаем продукт из запроса по его ИД 
    product = get_object_or_404(Products, id=product_id)
    # получаем объект заполненной формы со странички
    form = CartAddProductForm(request.POST)

    # если форма заполнена правильно        
    if form.is_valid():
        cd = form.cleaned_data
        # вызываем метод добавления товара в корзину с введенным в поле количеством
        cart.add(product=product, 
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    # если форма не заполнена
    else:
        # добавляем  1 единицу товара
        cart.add(product=product, 
                 quantity=1,
                 override_quantity=False)
    # переходим на страницу корзины
    return redirect('cart:cart-detail')


# удаление товара из корзины
@require_POST
def remove_from_db(request, product_id):
    cart = ProductCartUser(request)
    del cart.cart[str(product_id)]
    
    cart.remove(product_id, request)    
    
    return redirect('cart:cart-detail')





@require_POST
@csrf_exempt
def get_ajax(request):
    data = json.loads(request.body)
    product_count = data.get('count')
    product_id = data.get('id')
    
    product = get_object_or_404(Products, id=product_id)
    product_item = CartItem.objects.get(product=product)
    product_item.quantity = product_count
    product_item.save()
    
    
    response_data = {'result': 'success'}
    return HttpResponse(json.dumps(response_data), content_type = 'application/json')