from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User


class SignupUser(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(SignupUser, self).create(validated_data)

    class Meta:
        model = User
        fields = '__all__'


class LoginUser(serializers.ModelSerializer):
    phonenumber = serializers.CharField()

    class Meta:
        model = User
        fields = ['phonenumber', 'password']


class ListUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
