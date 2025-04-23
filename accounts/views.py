import uuid
from random import randint
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
import random
import string
import ghasedak_sms
from .models import User, Otp
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
import re
from django.shortcuts import render, redirect, reverse
from uuid import uuid4
from django.views import View
from .forms import LogimForm, RegisterForm, ChekOtpForm, CompeletProfile, ProfileUpdateForm
import requests
import json
from django.contrib.auth.decorators import login_required

Ghasedack = ghasedak_sms.Ghasedak
API_KEY = "35a3e8b000ce1ed436329a2796b38e634ca4f35bfb9f7adb2cd91ee64cbc26f5kdbHYwiRyWt7bbMz"  # کلید API خود را وارد
sms_api = "35a3e8b000ce1ed436329a2796b38e634ca4f35bfb9f7adb2cd91ee64cbc26f5kdbHYwiRyWt7bbMz"  # کلید API خود را وارد


# کنید
# URL = "https://gateway.ghasedak.me/rest/api/v1/WebService/SendOtpWithParams"
# ky = ghasedak_sms.Ghasedak(baseurl=API_KEY, apikey=sms_api)


def phone_number_validator(value):
    """Validator برای شماره تلفن که ابتدا با 09 شروع شود و 11 رقم باشد"""
    if not value.startswith('09'):
        raise ValidationError('شماره تلفن باید با 09 شروع شود.')
    if len(value) != 11:
        raise ValidationError('شماره تلفن باید 11 رقم باشد.')
    if not re.match(r'^\d{11}$', value):
        raise ValidationError('شماره تلفن باید فقط از اعداد تشکیل شود.')


class UserLogin(View):
    def get(self, request, *args, **kwargs):
        form = LogimForm()
        return render(request, 'accounts/send_code.html', {'form': form})

    def post(self, request):
        form = LogimForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone = cd['phone']

            # اعتبارسنجی شماره تلفن
            try:
                phone_number_validator(phone)
            except ValidationError as e:
                # در صورت خطا، پیام خطا را به قالب ارسال می‌کنیم
                return render(request, 'accounts/send_code.html', {'form': form, 'error': e.message})

            # اگر شماره تلفن معتبر باشد، ورود انجام می‌شود
            user = authenticate(username=phone)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error('phone', 'شماره تلفن است')
        else:
            form.add_error('phone', 'شماره تلفن است')

        return render(request, 'accounts/send_code.html', {'form': form})


class OtpLoginView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, 'accounts/otplogin.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone = cd['phone']

            # اعتبارسنجی شماره تلفن در همین ویو
            if not phone.startswith('09'):
                messages.error(request, 'شماره تلفن باید با 09 شروع شود.')
                return render(request, 'accounts/otplogin.html', {'form': form})

            if len(phone) != 11:
                messages.error(request, 'شماره تلفن باید 11 رقم باشد.')
                return render(request, 'accounts/otplogin.html', {'form': form})

            if not re.match(r'^\d{11}$', phone):
                messages.error(request, 'شماره تلفن باید فقط شامل اعداد باشد.')
                return render(request, 'accounts/otplogin.html', {'form': form})

            # اگر شماره معتبر بود، ارسال کد انجام شود
            randcode = randint(1000, 9999)
            token = str(uuid4())

            send_otp(phone, randcode)  # فرض می‌کنیم این تابع پیامک ارسال می‌کند
            Otp.objects.create(phone=phone, code=randcode, token=token)

            messages.success(request, 'کد تأیید برای شما ارسال شد.')
            return redirect(reverse('verify_code') + f'?token={token}')

        else:
            messages.error(request, 'فرم معتبر نیست. لطفاً اطلاعات را بررسی کنید.')

        return render(request, 'accounts/otplogin.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.error(request, '⛔ با موقیت خارج شدید.')
    return redirect('/')


class ChekOtp(View):
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        print(f"توکن دریافتی: {token}")  # نمایش مقدار توکن در لاگ سرور

        if not token:
            messages.error(request, "توکن معتبر نیست!")
            return redirect('/')

        try:
            otp = Otp.objects.get(token=token)
        except Otp.DoesNotExist:
            messages.error(request, "کد تأیید یافت نشد یا منقضی شده است!")
            return redirect('/')

        form = ChekOtpForm(token=token)
        otp_expired = otp.is_expired()
        if otp_expired:
            otp.delete()

        return render(request, 'accounts/verify_code.html', {'form': form, 'otp_expired': otp_expired, 'token': token})

    def post(self, request):
        token = request.GET.get('token')
        if not token:
            messages.error(request, "توکن معتبر نیست!")
            return redirect('/')

        form = ChekOtpForm(request.POST, token=token)

        if form.is_valid():
            otp = Otp.objects.get(token=token)

            if otp.is_expired():
                messages.error(request, "کد منقضی شده است، لطفاً مجدداً درخواست دهید.")
                return redirect(reverse('resend_otp') + f'?token={token}')

            user, created = User.objects.get_or_create(phone=otp.phone)

            if not user.first_name or not user.last_name:
                return redirect(reverse('nameuser') + f'?token={token}')

            login(request, user)

            messages.success(request, "با موفقیت وارد شدید!")
            return redirect('/')

        return render(request, 'accounts/verify_code.html', {'form': form})


class CompleteProfileView(View):
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        if token:
            try:
                otp = Otp.objects.get(token=token)
                if otp.created_at + timezone.timedelta(minutes=3) < timezone.now():
                    otp.delete()
                    messages.error(request, '⛔ کد تأیید منقضی شده است.')
                    return redirect(reverse('OtpLogin'))
                phone = otp.phone
                form = CompeletProfile()
                return render(request, 'accounts/name.html', {'form': form, 'phone': phone, 'token': token})
            except Otp.DoesNotExist:
                messages.error(request, '⛔ توکن نامعتبر است.')
                return redirect('/')
        messages.error(request, '⛔ توکن وجود ندارد.')
        return redirect('/')

    def post(self, request, *args, **kwargs):
        token = request.GET.get('token')
        if token:
            try:
                otp = Otp.objects.get(token=token)
                if otp.created_at + timezone.timedelta(minutes=3) < timezone.now():
                    otp.delete()
                    messages.error(request, '⛔ کد تأیید منقضی شده است.')
                    return redirect(reverse('OtpLogin'))

                form = CompeletProfile(request.POST)
                if form.is_valid():
                    user = User.objects.get(phone=otp.phone)
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.save()
                    otp.delete()  # حذف OTP پس از تکمیل پروفایل
                    login(request, user)
                    param1 = user.first_name + ' ' + user.last_name
                    phone = user.phone
                    # ارسال پیام خوش‌آمدگویی پس از تکمیل پروفایل
                    send_welcome_sms(phone, param1)

                    messages.success(request, '✅ پروفایل شما با موفقیت تکمیل شد.')
                    return redirect('/')
                else:
                    messages.error(request, '⛔ لطفا تمام فیلدها را تکمیل کنید.')

            except Otp.DoesNotExist:
                messages.error(request, '⛔ توکن نامعتبر است.')
                return redirect('/')
        messages.error(request, '⛔ توکن وجود ندارد.')
        return redirect('/')


def profile_update_view(request):
    next_url = request.GET.get('next', '/')

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            form.save()
            messages.success(request, '✅ پروفایل شما با موفقیت به‌روزرسانی شد.')
            return redirect(next_url)

    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile_update.html', {'form': form, 'next': next_url})


def resend_otp(request):
    token = request.GET.get('token')
    print(f"توکن دریافتی برای ارسال مجدد: {token}")  # نمایش مقدار توکن در لاگ

    if not token:
        messages.error(request, "توکن معتبر نیست!")
        return redirect('/')

    try:
        otp = Otp.objects.get(token=token)
    except Otp.DoesNotExist:
        messages.error(request, "کد تأیید یافت نشد!")
        return redirect('/')

    # حذف OTP قدیمی
    otp.delete()

    # ایجاد OTP جدید
    new_code = randint(1000, 9999)
    new_token = str(uuid4())

    send_otp(otp.phone, new_code)

    new_otp = Otp.objects.create(phone=otp.phone, code=new_code, token=new_token)

    messages.success(request, "کد تأیید جدید برای شما ارسال شد!")
    return redirect(reverse('verify_code') + f'?token={new_token}')


URL = "https://gateway.ghasedak.me/rest/api/v1/WebService/SendOtpWithParams"
api_key = '35a3e8b000ce1ed436329a2796b38e634ca4f35bfb9f7adb2cd91ee64cbc26f5kdbHYwiRyWt7bbMz'


#----------- پنل پیامکی-----------------
def send_otp(mobile, param1, ):
    url = URL

    print(f"Sending OTP to: {mobile}, Code: {param1}")

    payload = json.dumps({
        "receptors": [
            {
                "mobile": str(mobile),
                "clientReferenceId": "1"
            }
        ],
        "templateName": "boleyla",
        "param1": str(param1),
        "lineNumber": "30005006004099",
        "isVoice": False,
        "udh": False,

    })
    headers = {
        'Content-Type': 'application/json',
        'ApiKey': api_key
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    # return render(response,'accounts/send_code.html')


def send_welcome_sms(phone, param1, ):
    """ارسال پیام خوش‌آمدگویی به شماره تلفن وارد شده."""
    url = URL
    payload = json.dumps({
        "receptors": [
            {
                "mobile": str(phone),
                "clientReferenceId": "1"
            }
        ],
        "templateName": "profile",
        "param1": param1,
        "lineNumber": "30005006004099",
        "isVoice": False,
        "udh": False,

    })
    headers = {
        'Content-Type': 'application/json',
        'ApiKey': 'f70caf7374448b254b53e8d960285173b85915e3b4129b2969266e77398ccdb6FTTqDzfg8uBmCGUy'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print("Response Status:", response.status_code)
    print("Response Data:", response.text)
    return response.status_code, response.text
