from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse
from django.views.generic import CreateView, ListView, DetailView

from cart.forms import CartAddProductForm
from .models import Category, SubCategory, Products
from .forms import CategoryForm, SubCategoryForm, ProductForm
from django.urls import reverse_lazy
from django import template

register = template.Library()


def index(request):
    category = Category.objects.all()
    context = {
        'category_list': category
    }

    return render(request, 'products/index.html', context=context)
   

class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'
    form = CategoryForm
    template_name = 'products/category-form.html'
    success_url = reverse_lazy('products:category-list')


class CategoryListView(ListView):
    model = Category
    template_name = 'products/category-list.html'
    context_object_name = 'categories'

   

class SubCategoryCreateView(CreateView):
    model = SubCategory
    fields = '__all__'
    form = SubCategoryForm
    template_name = 'products/subcategory-form.html'
    success_url = reverse_lazy('products:category-list')



def CategoryDetail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcategory = SubCategory.objects.filter(category=category)
    context = {
        'category': category,
        'subcategory': subcategory
    }

    return render(request, 'products/category-detail.html', context=context)



class ProductCreateView(CreateView):
    model = Products
    fields = '__all__'
    form = ProductForm
    template_name = 'products/product-form.html'
    success_url = reverse_lazy('products:index')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['subcategories'] = SubCategory.objects.all()
        return context

    def form_valid(self, form):
        self.instance = form.save(commit=False)
        self.instance.category_id = self.request.POST.get('category')
        self.instance.subcategory_id = self.request.POST.get('subcategory')
        self.instance.save()
        return super().form_valid(form)


class ProductListView(ListView):
    model = Products
    template_name = 'products/product-list.html'
    context_object_name = 'products'


    def get_queryset(self):
        super().get_queryset()
        slug = self.request.resolver_match.kwargs['subcat_slug']
        queryset = Products.objects.filter(subcategory__slug = slug)
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        context['cart_product_form'] = cart_product_form
        return context

       

class ProductDetailView(DetailView):
    model = Products
    template_name = 'products/product-detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'prod_slug'
    

    
    
    

