from django.contrib import admin
from . import models
from accounts.models import User


# متد برای نمایش آدرس
def get_address(obj):
    return obj.address.address  # نمایش آدرس


get_address.short_description = 'Address'  # تغییر نام نمایش آدرس در پنل ادمین


# ثبت مدل‌ها در پنل ادمین
class OrderItemAdmin(admin.TabularInline):
    model = models.OrderItem


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'address', 'phone', 'is_paid')
    inlines = [OrderItemAdmin]
    list_filter = ('is_paid',)

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    full_name.short_description = "نام کامل"


# @admin.register(models.Address)
# class AddressAdmin(admin.ModelAdmin):
#     list_display = ('user', 'address')  # لیست نمایش فیلدهای آدرس
