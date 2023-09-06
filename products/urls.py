from django.urls import path
from .views import *


app_name = 'products'
urlpatterns = [
    path('', index, name='index'),
    path('category-form/', CategoryCreateView.as_view(), name='category-form'),
    path('category-list/', CategoryListView.as_view(), name='category-list'),
    
    path('subcategory-form/', SubCategoryCreateView.as_view(), name='subcategory-form'),
        
    path('product-form/', ProductCreateView.as_view(), name='product-form'),
    path('product-list/<slug:cat_slug>/<slug:subcat_slug>/', ProductListView.as_view(), name='product-list'),
    path('product-detail/<slug:cat_slug>/<slug:subcat_slug>/<slug:prod_slug>/', ProductDetailView.as_view(), name='product-detail'),

    
]
