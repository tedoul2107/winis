import hashlib

from rest_framework.serializers import ModelSerializer
from .models import Category, SubCategory


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
