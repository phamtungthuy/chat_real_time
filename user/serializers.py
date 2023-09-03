from rest_framework import serializers
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_serializer
from django.core.validators import RegexValidator
import re
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
    # def validate(self, data):
    #     for key, value in data.items():
    #         print(value)
    #         if ' ' in value:
    #             raise serializers.ValidationError(f'{key} must not contain blank')
    #         elif value == '':
    #             raise serializers.ValidationError(f'{key} must not be blank')
    #     return data


    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Username must be at least 3 characters')
        return value
    
    def validate_password(self, value):
        if len(value) < 7:
            raise serializers.ValidationError('Password must be at least 7 characters')
        return value
