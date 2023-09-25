import uuid
from django.db import models

STATUS_CHOICES = (
    ("confirmed", "Подтвержден"),
    ("waiting_payment", "Ожидает оплаты"),
    ("paid", "Оплачен"),
    ("assembly", "Собирается"),
    ("on_way", "В пути"),
    ("delivery_point", "В пунке выдачи"),
    ("delivered", "Доставлен"),
    ("canceled", "Отменен"),
)


class Order(models.Model):
    number = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    first_name = models.CharField(max_length=256, verbose_name='Имя')
    last_name = models.CharField(max_length=256, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Электронная почта')
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    address = models.TextField(verbose_name="Адрес")
    status = models.CharField(choices=STATUS_CHOICES)
    payment = models.CharField(max_length=50, verbose_name='Способ оплаты')
    deliviry = models.CharField(max_length=50, verbose_name='Способ доставки')

    
    def __str__(self):
        return " ".join(["order_",self.number])
    
    