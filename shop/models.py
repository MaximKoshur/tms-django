from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        INITIAL = 'INITIAL', 'Initial'
        COMPLETED = 'COMPLETED', 'Completed'
        DELIVERED = 'DELIVERED', 'Delivered'

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INITIAL)

    def total_price(self):
        total_price = 0
        for entry in self.order_entries.all():
            total_price += entry.product.price * entry.count
        return total_price

    def total_count(self):
        total_count = 0
        for entry in self.order_entries.all():
            total_count += entry.count
        return total_count


class OrderEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='+')
    count = models.IntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_entries')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shopping_cart = models.OneToOneField(Order, on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='+')

    def __str__(self):
        return self.user.username

