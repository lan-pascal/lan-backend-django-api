from django.urls import path, include
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', "first_name", "last_name", 'email', "password")
        extra_kwargs = {
            'password': {'write_only': True}
        }

class UserSignUpSerializer(serializers.ModelSerializer):
    email_confirm = serializers.EmailField(label="Confirm Email",  required=True)
    password_confirm = serializers.CharField(label="Confirm Password", required=True)
    class Meta:
        model = User
        fields = ('username', "first_name", "last_name", 'email',"email_confirm", "password","password_confirm")
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email_confirm(self, value):
        data = self.get_initial()
        email = data.get("email")
        email_confirm = value
        if email != email_confirm:
            raise ValidationError("The emails don't match!", code="email_confirmation_error")
        return value

    def validate_password_confirm(self, value):
        data = self.get_initial()
        password = data.get("password")
        password_confirm = value
        if password != password_confirm:
            raise ValidationError("The passwords don't match!", code="password_confirmation_error")
        return value
    
    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]

        user = User(
            username = username,
            email = email,
            )
        user.set_password(password)
        user.save()

        return validated_data

class UserSignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',"password")
        extra_kwargs = {
            'password': {'write_only': True}
        }