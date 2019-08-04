from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator    

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..conf import settings, AuthMethod

User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
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

class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username","email","password")
        extra_kwargs = {
            'username': 
            {
                'required ': settings.AUTH_BACKEND_METHOD == (AuthMethod.USERNAME | AuthMethod.USERNAME_EMAIL)
            },
            'email' : 
            {
                'required' : settings.AUTH_BACKEND_METHOD == (AuthMethod.EMAIL | AuthMethod.USERNAME_EMAIL)
            },
            'password': {'write_only': True}
        }

    def validate(self, data):
        username = data["username"]
        email = data["email"]
        password = data["passsword"]

        user = authenticate(self.data["request"],username=username,email=email,password=password)
        
        if user:
            if not user.is_active:
                raise ValidationError("This user account is inactive") 
        else:
            raise ValidationError("You were unable to sign in with the provided credentials")

        data['user'] = user
        return value

    
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(label="Old Password", required=True)
    new_password1 = serializers.CharField(label="New Password", required=True)
    new_password2 = serializers.CharField(label="Confirm New Password", required=True)

    password_change_form_class = PasswordChangeForm

    def __init__(self, *args, **kwargs):
        self.request = self.context.request
        self.user = getattr(self.request,"user", None)

    def validate(self,data):
        self.password_change_form = self.password_change_form_class(
            user=self.user, data=data
        )
        
        if not self.password_change_form.is_valid():
            return ValidationError(self.password_change_form.errors)
        
        return data

    def save(self):
        self.form_password_change.save()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    email_template_subject = "registration/email/password_reset_subject.txt"
    email_template_body = "registration/email/password_reset_body.html"

    password_rest_form_class = PasswordResetForm

    def validate(self,data):
        self.password_rest_form = self.password_rest_form_class(data=data)
        
        if not self.password_rest_form.is_valid():
            return ValidationError(self.password_rest_form.errors)
        
        return data

    def save(self):
        kwargs = {
            'use_https': request.is_secure(),
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'request': request,
            "subject_template_name": email_template_subject,
            "email_template_name": email_template_body
        }
        self.form_password_reset.save(**kwargs)

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

        self.set_password_form_class = self.set_password_form_class(
            user=user, data=data
        )
        
        if not self.set_password_form_class.is_valid():
            raise ValidationError(self.set_password_form_class.errors)
        
        return data


    def save(self):
        self.set_password_form_class.save()

    def _get_user(self,uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            raise ValidationError({'uid': ['Invalid value']})

        return user
