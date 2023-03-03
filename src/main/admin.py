from django.contrib import admin

from main.models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(StockVariation)
