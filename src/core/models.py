from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True, default=uuid.uuid1)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    ADMIN = 'ADMIN'
    STOCK_MANAGER = 'STOCK_MANAGER'
    ONLINE_SALE_MANAGER = 'ONLINE_SALE_MANAGER'

    ROLE_TYPE_CHOICES = [
        (ADMIN, 'ADMIN'),
        (STOCK_MANAGER, 'STOCK_MANAGER'),
        (ONLINE_SALE_MANAGER, 'ONLINE_SALE_MANAGER'),
    ]
    role = models.CharField(
        max_length=255,
        choices=ROLE_TYPE_CHOICES
    )

    eTag = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    first_name = None
    last_name = None
    email = None

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.name} {self.username} {self.role} {self.created_at} {self.updated_at}"
