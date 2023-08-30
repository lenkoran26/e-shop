from django.urls import path
from .views import *


app_name = 'products'
urlpatterns = [
    path('', index, name='index'),
    path('category-form/', CategoryCreateView.as_view(), name='category-form'),
    path('category-list/', CategoryListView.as_view(), name='category-list'),
    path('subcategory-form/', SubCategoryCreateView.as_view(), name='subcategory-form'),
    path('category/<slug:category_slug>/', CategoryDetail, name='category-detail'),
    path('product-form/', ProductCreateView.as_view(), name='product-form'),
]