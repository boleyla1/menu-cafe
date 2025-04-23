# cafe_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('setting/', views.settings_view, name='setting'),
    path('categories/', views.categories, name='categories'),
    path('categories/delete/<int:id>/', views.delete_category, name='delete_category'),
    path('categories/update/<int:id>/', views.update_category, name='update_category'),
    path('products/', views.products, name='products'),
    path('products/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('products/update/<int:id>/', views.update_product, name='update_product'),
    path('search/', views.product_list_view, name='product_list_view'),
    path('products/<int:id>/', views.products, name='product_id'),
]