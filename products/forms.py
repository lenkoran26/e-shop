from django import forms
from .models import Category, SubCategory, Products


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'slug': 'Url-адрес',
        }


class SubCategoryForm(forms.ModelForm):
    # category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='None')
    class Meta:
        model = SubCategory
        fields = '__all__'
        labels = {
            'name': 'Подкатегория',
            'category': 'Категория',
        }


class ProductForm(forms.ModelForm):
    category = forms.SelectMultiple()
    subcategory = forms.SelectMultiple()
    class Meta:
        model = Products
        exclude = ['created_at', 'is_available', 'subcategory']