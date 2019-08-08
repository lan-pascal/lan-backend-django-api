from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator    

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CurrentUserDefault

from ..conf import settings

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', "first_name", "last_name", 'email', "password")
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]

        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]

        user = User(
            username = username,
            email = email,
            first_name = first_name,
            last_name = last_name,
            )
        user.set_password(password)
        user.save()

        return user
    
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(label="Old Password", required=True)
    new_password1 = serializers.CharField(label="New Password", required=True)
    new_password2 = serializers.CharField(label="Confirm New Password", required=True)

    password_change_form_class = PasswordChangeForm

    def validate(self,data):
        user = self.context["request"].user

        self.password_change_form = self.password_change_form_class(
            user=user, data=data
        )
        
        if not self.password_change_form.is_valid():
            return ValidationError(self.password_change_form.errors)
        
        return data

    def save(self):
        self.password_change_form.save()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    email_template_subject = "registration/email/password_reset_subject.txt"
    email_template_body = "registration/email/password_reset_body.html"

    password_reset_form_class = PasswordResetForm

    def __init__(self, *args, **kwargs):
        super().__init__(args,kwargs)
        print(self)
        self.request = kwargs["context"]["request"]
        print(self)

    def validate(self,data):
        self.password_reset_form = self.password_reset_form_class(data=data)
        if not self.password_reset_form.is_valid():
            return ValidationError(self.password_reset_form.errors)
        
        return data

    def save(self):
        kwargs = {
            'use_https': self.request.is_secure(),
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'request': self.request,
            "subject_template_name": email_template_subject,
            "email_template_name": email_template_body
        }
        self.password_reset_form.save(**kwargs)

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password1  = serializers.CharField(required=True)
    new_password2  = serializers.CharField(required=True)
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    set_password_form_class = SetPasswordForm
    token_generator = default_token_generator

    def validate(self,data):
        uidb64 = data["uidb64"]
        token = data["token"]

        user = _get_user(uidb64)

        if not self.token_generator.check_token(user,token):
            raise ValidationError({"invalid_token":"The token provided is invalid!"})

        self.set_password_form = self.set_password_form_class(
            user=user, data=data
        )
        
        if not self.set_password_form.is_valid():
            raise ValidationError(self.set_password_form.errors)
        
        return data


    def save(self):
        self.set_password_form.save()

    def _get_user(self,uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            raise ValidationError({'uid': ['Invalid value']})

        return user
