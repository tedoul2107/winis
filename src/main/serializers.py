import hashlib

from rest_framework.serializers import ModelSerializer
from .models import Category, SubCategory, Product, StockVariation


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'base_curve', 'diameter', 'power', 'material', 'water_content', 'package', 'eTag']
        extra_kwargs = {
            'eTag': {"read_only": True}
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.eTag = hashlib.md5(instance.contract().encode('utf-8')).hexdigest()
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.base_curve = validated_data.get('base_curve', instance.base_curve)
        instance.diameter = validated_data.get('diameter', instance.diameter)
        instance.power = validated_data.get('power', instance.power)
        instance.material = validated_data.get('material', instance.material)
        instance.water_content = validated_data.get('water_content', instance.water_content)
        instance.package = validated_data.get('package', instance.package)
        instance.eTag = hashlib.md5(instance.contract().encode('utf-8')).hexdigest()

        instance.save()
        return instance


class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'categoryId', 'name', 'n_tone', 'cycle_period', 'eTag']
        extra_kwargs = {
            'eTag': {"read_only": True}
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.eTag = hashlib.md5(instance.contract().encode('utf-8')).hexdigest()
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.categoryId = validated_data.get('categoryId', instance.categoryId)
        instance.name = validated_data.get('name', instance.name)
        instance.n_tone = validated_data.get('n_tone', instance.n_tone)
        instance.cycle_period = validated_data.get('cycle_period', instance.cycle_period)
        instance.eTag = hashlib.md5(instance.contract().encode('utf-8')).hexdigest()

        instance.save()
        return instance


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'subcategoryId', 'model', 'color', 'image', 'quantity', 'eTag']
        extra_kwargs = {
            'eTag': {"read_only": True}
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.eTag = hashlib.md5(instance.contract().encode('utf-8')).hexdigest()
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.subcategoryId = validated_data.get('subcategoryId', instance.subcategoryId)
        instance.model = validated_data.get('model', instance.model)
        instance.color = validated_data.get('color', instance.color)
        instance.image = validated_data.get('image', instance.image)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.eTag = hashlib.md5(instance.contract().encode('utf-8')).hexdigest()

        instance.save()
        return instance


class StockVariationSerializer(ModelSerializer):
    class Meta:
        model = StockVariation
        fields = ['id', 'productId', 'type', 'quantity', 'datetime', 'updated_at', 'status', 'userId', 'eTag']
        extra_kwargs = {
            'eTag': {"read_only": True}
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.eTag = hashlib.md5(instance.contract().encode('utf-8')).hexdigest()
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.eTag = hashlib.md5(instance.contract().encode('utf-8')).hexdigest()

        instance.save()
        return instance
