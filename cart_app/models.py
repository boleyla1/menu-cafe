from django.db import models
from accounts.models import User
from cafe_app.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=1000, blank=False, null=False)
    phone = models.CharField(max_length=12)
    total_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.phone


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    quantity = models.SmallIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.product.name
