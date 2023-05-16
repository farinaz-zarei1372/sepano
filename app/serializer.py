from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Usermodel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class SignupUser(serializers.ModelSerializer):
    # user = UserSerializer(many=True)

    def create(self, validated_data):
        validated_data["password"] = validated_data.get("password")
        return super(SignupUser, self).create(validated_data)

    class Meta:
        model = Usermodel
        fields = '__all__'


class LoginUser(serializers.ModelSerializer):
    phonenumber = serializers.IntegerField()

    class Meta:
        model = Usermodel
        fields = ['phonenumber', 'password']


class ListUser(serializers.ModelSerializer):
    class Meta:
        model = Usermodel
        fields = '__all__'
