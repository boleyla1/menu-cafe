from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart-add/', views.cartadd, name='cart_add'),
    path('cart-delete/', views.cart_delete, name='cart_delete'),
]