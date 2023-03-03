import os

from django.db import models
from django.dispatch import receiver
from core.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    base_curve = models.FloatField(default=8.6)
    diameter = models.FloatField(max_length=255)
    power = models.FloatField(max_length=255, default=0.00)
    material = models.CharField(max_length=255, default='HEMA')
    water_content = models.FloatField(max_length=255, default=38)
    package = models.CharField(max_length=500, default='2 lenses + 1 case')
    eTag = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def contract(self):
        return f'{self.name} {self.base_curve} {self.diameter} {self.power} {self.material} ' \
               f'{self.water_content} {self.package} {self.created_at} {self.updated_at}'


class SubCategory(models.Model):
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    n_tone = models.IntegerField()
    cycle_period = models.CharField(max_length=255)

    eTag = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def contract(self):
        return f'{self.categoryId} {self.name} {self.n_tone} {self.cycle_period} {self.created_at} {self.updated_at}'


class Product(models.Model):
    subcategoryId = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    image = models.ImageField(blank=True)
    quantity = models.IntegerField()

    eTag = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.model

    def contract(self):
        return f'{self.model} {self.color} {self.quantity} {self.created_at} {self.updated_at}'


class StockVariation(models.Model):
    productId = models.ForeignKey(Product, on_delete=models.CASCADE)

    PLUS = 'PLUS'
    MINUS = 'MINUS'

    STOCK_TYPE_CHOICES = [
        (PLUS, 'PLUS'),
        (MINUS, 'MINUS'),
    ]

    type = models.CharField(
        max_length=20,
        choices=STOCK_TYPE_CHOICES,
        default=MINUS,
    )

    quantity = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    PENDING = 'PENDING'
    CANCELLED = 'CANCELLED'
    VALIDATED = 'VALIDATED'

    STOCK_STATUS_CHOICES = [
        (PENDING, 'PENDING'),
        (CANCELLED, 'CANCELLED'),
        (VALIDATED, 'VALIDATED')
    ]

    status = models.CharField(
        max_length=25,
        choices=STOCK_STATUS_CHOICES,
        default=PENDING,
    )

    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    eTag = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.productId} {self.type} {self.quantity} {self.status}'

    def contract(self):
        return f'{self.productId} {self.type} {self.quantity} {self.quantity} {self.datetime} {self.userId} {self.updated_at}'


@receiver(models.signals.post_delete, sender=Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=Product)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Product.objects.get(pk=instance.pk).image
    except Product.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
