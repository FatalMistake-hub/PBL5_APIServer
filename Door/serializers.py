from django.core.files.base import File
from rest_framework import serializers
from rest_framework.fields import ImageField

from .models import  Door, Users


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=125)
    
class UserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    full_name = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    user_type = serializers.CharField(max_length=50)
    gender = serializers.CharField(max_length=10)
    birthday = serializers.DateField()
class DoorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Door
        fields = ('name', 'status', 'time')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

