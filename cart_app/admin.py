from django.contrib import admin
from  . import models

class OrderItemAdmin(admin.TabularInline):
    model = models.OrderItem
# Register your models here.

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone','is_paid')
    inlines = [OrderItemAdmin]
    list_filter = ('is_paid',)