from django.contrib import admin
from .models import Category,CafeSettings,Product

admin.site.register(Category)
admin.site.register(CafeSettings)
admin.site.register(Product)

# Register your models here.
