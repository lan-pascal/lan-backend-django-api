from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate

from django_registration import forms as django_registration_forms

User = get_user_model()

class RegistrationForm(django_registration_forms.RegistrationFormUniqueEmail):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta(django_registration_forms.RegistrationForm.Meta):
        model = User
        fields = [
            "first_name",
            "last_name",
            User.USERNAME_FIELD,
            User.get_email_field_name(),
            "password1",
            "password2",
        ]
    