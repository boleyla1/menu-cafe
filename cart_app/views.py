from django.shortcuts import render, get_object_or_404
from django.views import View
from django.conf import settings
import requests
import json
from .cart import Cart
from cart_app.models import *
from django.http import JsonResponse
from django.contrib import messages


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        product = cart.get_prods()
        quantities = cart.get_quants()  # دریافت مقدار تعداد محصول از سبد خرید

        return render(request, 'cart_app/cart.html', {
            "product": product,
            "quantities": quantities,
            'cart': cart,

        })


def cartadd(request):
    cart = Cart(request)
    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)

        # بررسی اینکه آیا محصول قبلاً به سبد خرید اضافه شده است
        if str(product_id) in cart.cart:  # باید بررسی کنیم که محصول به صورت string ذخیره شده
            response = {
                'message': f"محصول {product.name} قبلاً به سبد خرید اضافه شده است.",
                'error': True
            }
        else:
            # اضافه کردن محصول به سبد خرید
            cart.add(product=product, quantity=product_qty)

            # محاسبه تعداد کل محصولات در سبد خرید
            cart_total_quantity = sum(int(qty) for qty in cart.cart.values())

            # ارسال پیام موفقیت
            response = {
                'message': f"محصول {product.name} با موفقیت به سبد خرید اضافه شد.",
                'cart_total_quantity': cart_total_quantity,
                'error': False
            }

        return JsonResponse(response)


def cart_delete(request):
    cart = Cart(request)
    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)

        # حذف محصول از سبد خرید
        cart.delete(product=product_id)

        # محاسبه تعداد محصولات باقی‌مانده در سبد خرید
        cart_total_quantity = sum(int(qty) for qty in cart.cart.values())

        # ارسال پیام موفقیت
        messages.success(request, f"{product.name} با موفقیت از سبد خرید حذف شد!")

        # ارسال پاسخ JSON شامل تعداد محصولات باقی‌مانده
        response = JsonResponse({
            'cart_total_quantity': cart_total_quantity,
            'message': f"{product.name} با موفقیت از سبد خرید حذف شد!"
        })
        return response

ZP_API_REQUEST = 'https://api.zarinpal.com/pg/v4/payment/request.json'
ZP_API_VERIFY = 'https://api.zarinpal.com/pg/v4/payment/verify.json'
ZP_API_STARTPAY = 'https://www.zarinpal.com/pg/StartPay/'

amount = 1000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/verify/'


def send_request(request):
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Description": description,
        "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                        'authority': response['Authority']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}
