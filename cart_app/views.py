from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
import requests
import json
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .cart import Cart
from cart_app.models import *
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from accounts.models import User


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        product = cart.get_prods()
        quantities = cart.get_quants()  # دریافت مقدار تعداد محصول از سبد خرید
        user = User.objects.all()

        return render(request, 'cart_app/cart.html', {
            "product": product,
            "quantities": quantities,
            'cart': cart,
            'user': user,

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
    user = User.objects.all()
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
        context = {
            'user': user
        }

        return response


class OrderView(View):
    def get(self, request, id):
        # دریافت سفارش براساس pk
        order = Order.objects.get(id=id)

        # ارسال اطلاعات به صفحه سفارش
        return render(request, 'cart_app/order_add.html', {
            'order': order
        })


class OrderCreation(View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=int(cart.total()))
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'],
                                     price=item['price'])
        return redirect('order_view', order.id)

    def post(self, request):
        cart = Cart(request)

        address = request.POST.get("address")
        phone = request.POST.get("phone")

        if not address:
            return render(request, 'cart_app/cart.html', {
                'error_message': 'آدرس الزامی است.'
            })

        order = Order.objects.create(
            user=request.user,
            total_price=int(cart.total()),
            phone=phone,
            address=address
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )

        return redirect('order_view', order.id)


MERCHANT = '9f22ca55-acd7-4b10-89f1-de1ea03d6e04'

ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{}"

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
callback_url = "http://127.0.0.1:8000/cart/payment/verify/"


class send_request(View):
    def get(self, request, pk):
        # پیدا کردن سفارش بر اساس شناسه (pk)
        order = get_object_or_404(Order, id=pk, user=request.user)
        request.session['order_id'] = str(order.id)

        # تبدیل مبلغ به ریال

        # داده‌ها برای درخواست به زرین‌پال
        data = {
            "merchant_id": settings.MERCHANT,
            "amount": order.total_price,  # از مبلغ سفارش استفاده کنید
            "currency": "IRT",
            "callback_url": callback_url,  # آدرس برگشت
            "description": description,  # توضیحات
            "metadata": {
                "mobile": order.user.phone  # شماره تلفن کاربر
            }
        }
        print("در حال ارسال داده به زرین‌پال:")
        print(json.dumps(data, indent=2))

        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        print("در حال ارسال داده به زرین‌پال:")
        print(json.dumps(data, indent=2))

        response = requests.post(
            ZP_API_REQUEST,
            data=json.dumps(data),
            headers=headers
        )

        print("کد وضعیت پاسخ:", response.status_code)
        print("متن پاسخ:", response.text)

        res_data = response.json()

        if "data" in res_data and "authority" in res_data["data"]:
            authority = res_data["data"]["authority"]
            return redirect(f"https://www.zarinpal.com/pg/StartPay/{authority}")
        else:
            error_message = res_data.get("errors", {}).get("message", "خطای نامشخص")
            return HttpResponse(f"خطا: {error_message}")


class verify_payment(View):
    def get(self, request):
        t_authority = request.GET.get("Authority")
        t_status = request.GET.get("Status")
        order_id = request.session['order_id']
        order = Order.objects.get(id=int(order_id))
        if request.GET.get('Status') == 'OK':
            req_header = {
                "accept": "application/json",
                "content-type": "application/json"
            }
            req_data = {
                "merchant_id": settings.MERCHANT,
                'amount': order.total_price,
                "authority": t_authority,
            }
            req = requests.post(url=ZP_API_VERIFY,data=json.dumps(req_data), headers=req_header)
            if len(req.json()["errors"]) == 0:
                t_status = req.json()["data"]["code"]
                if t_status == 100:
                    order.is_paid = True
                    order.save()
                    return redirect('cart')
                elif t_status == 101:
                    return HttpResponse('tranction subbmited')
                else:
                    return HttpResponse('faild')
            else:
                e_code = req.json()["errors"]["code"]
                e_msg = req.json()["errors"]["message"]
                return HttpResponse(f'{e_code}: {e_msg}')
        else:
            return HttpResponse('cancled')