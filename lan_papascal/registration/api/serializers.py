from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm

from rest_framework.views import generics
from rest_framework.exceptions import ValidationError

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
                'required': settings.AUTH_BACKEND_METHOD == AuthMethod.USERNAME or settings.AUTH_BACKEND_METHOD == AuthMethod.USERNAME_EMAIL
            },
            'email' : 
            {
                'required' : settings.AUTH_BACKEND_METHOD == AuthMethod.EMAIL or settings.AUTH_BACKEND_METHOD == AuthMethod.USERNAME_EMAIL
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
        else
            raise ValidationError("You were unable to sign in with the provided credentials")

        data['user'] = user
        return value

    
class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(label="Old Password", required=True)
    new_password1 = serializers.CharField(label="New Password", required=True)
    new_password2 = serializers.CharField(label="Confirm New Password", required=True)

    form_password_change_class = PasswordChangeForm

    class Meta:
        model = User
        fields = ("old_password","new_password","new_password_confirm")}

    def __init__(self, *args, **kwargs):
        self.request = self.context.request
        self.user = getattr(self.request,"user", None)

    def validate(self,data):
        self.form_password_change = self.form_password_change_class(
            user=self.user, data=data
        )
        
        if not self.form_password_change.is_valid():
            return ValidationError(self.form_password_change.errors)
        
        return data

    def save(self):
        self.form_password_change.save()
