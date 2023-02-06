from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    base_curve = models.FloatField(max_length=255, default=8.6)
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
