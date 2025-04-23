from django.db import models

from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ingredients = models.TextField()
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class CafeSettings(models.Model):
    name = models.CharField(max_length=100, default="کافه بلیلا")
    address = models.TextField(default='مازندران')
    phone_number = models.CharField(max_length=15, default="09965759902")
    instagram_handle = models.CharField(max_length=50, default='mehrshad.boleyla')

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # phone = models.ForeignKey(User.phone, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=300, null=False)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product