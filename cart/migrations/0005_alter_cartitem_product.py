# Generated by Django 4.2.4 on 2023-09-22 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '__first__'),
        ('cart', '0004_alter_cartitem_cart_alter_cartitem_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.products'),
        ),
    ]
