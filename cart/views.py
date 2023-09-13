from market import settings
from products.models import Products
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Products
from .forms import CartAddProductForm
from cart.models import CartUser, CartItem

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
        
        # if self.user:
        #     user_cart = CartUser.objects.get_or_create(user=self.user)[0]
        #     for product_id in list(self.cart.keys()):
        #         product = Products.objects.get(pk=product_id)
        #         quantity = self.cart[str(product.id)]['quantity']
        #         cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product, quantity=quantity)
        #         if not created:
        #             cart_item.quantity += 1
        #             cart_item.save()
                
    

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
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    form = CartAddProductForm(request.POST)
    
    #добавление со страницы карточка товара
    #проверяем количество полей формы
    #если поле 1, то количество товара не передано, значит добавляем одну позицию
    
    if len(request.POST) == 1:
        cart.add(product=product, 
                 quantity=1,
                 override_quantity=False)
        return redirect('cart:cart-detail')
        
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, 
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    
    return redirect('cart:cart-detail')



@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, id=product_id)
    cart.remove(product)
    
    return redirect('cart:cart-detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    return render(request, 'cart/cart-detail.html', {'cart': cart})