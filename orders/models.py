from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import datetime

from cart.models import Products

STATUS_CHOICES = (
    ("in_process", "В обработке"),
    ("confirmed", "Подтвержден"),
    ("waiting_payment", "Ожидает оплаты"),
    ("paid", "Оплачен"),
    ("assembly", "Собирается"),
    ("on_way", "В пути"),
    ("delivery_point", "В пунке выдачи"),
    ("delivered", "Доставлен"),
    ("canceled", "Отменен"),
)

def get_order_number():
    date = datetime.now().strftime('%Y-%m-%d')
    if Order.objects.all().last():
        last_order = Order.objects.order_by('created_at').last()
        #last_order = Order.objects.all().last()
        if last_order.number[0:10] == date:
            num = int(last_order.number[11::]) + 1
        else:
            num = 1
    else:
        return f'{date}-1'
    return f'{date}-{num}'


class Order(models.Model):
    number = models.CharField(primary_key=True, unique=True, max_length=256, default=get_order_number, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, editable=False)
    first_name = models.CharField(max_length=256, verbose_name='Имя')
    last_name = models.CharField(max_length=256, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Электронная почта')
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    address = models.TextField(verbose_name="Адрес")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='in_process')
    payment = models.CharField(max_length=50, verbose_name='Способ оплаты')
    deliviry = models.CharField(max_length=50, verbose_name='Способ доставки')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма заказа', default=0)
    
    
    def __str__(self):
        return " ".join(["order_",self.number])
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField()
    
    def get_total_price(self):
        return self.product.price * int(self.quantity)
    