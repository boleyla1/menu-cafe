from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart-add/', views.cartadd, name='cart_add'),
    path('cart-delete/', views.cart_delete, name='cart_delete'),
    path('order/add', views.OrderCreation.as_view(), name='order_add'),
    path('cart/order/<int:id>/', views.OrderView.as_view(), name='order_view'),
    path('send_request/<int:pk>', views.send_request.as_view(), name='send_request'),
    path('payment/verify/', views.verify_payment.as_view(), name='verify_payment'),

]