import datetime

from rest_framework.serializers import ModelSerializer
from .models import User
import hashlib


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'password', 'role', 'eTag']
        extra_kwargs = {
            'password': {"write_only": True},
            'eTag': {"read_only": True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
            instance.eTag = hashlib.md5(instance.__str__().encode('utf-8')).hexdigest()

        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        if password is not None:
            instance.name = validated_data.get('name', instance.name)
            instance.username = validated_data.get('username', instance.username)
            instance.role = validated_data.get('role', instance.role)
            instance.set_password(password)
            instance.eTag = hashlib.md5(instance.__str__().encode('utf-8')).hexdigest()
            instance.is_active = False

        instance.save()
        return instance


