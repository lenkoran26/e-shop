from django.db import models
from django.contrib.auth.models import User
from products.models import Products


class CartUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(CartUser, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField()