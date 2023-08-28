from django.urls import path
from .views import index, CategoryCreateView, CategoryListView


app_name = 'products'
urlpatterns = [
    path('', index, name='index'),
    path('category-form/', CategoryCreateView.as_view(), name='category-form'),
    path('category-list/', CategoryListView.as_view(), name='category-list'),
]