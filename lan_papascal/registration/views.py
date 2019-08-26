from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login as auth_login
)

from . import forms

# Create your views here.
class SignUpView(LoginView):
    form_class = forms.SignUpForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        form.save()
        form.process_authenticate()
        return super().form_valid(form)


class SignInView(LoginView):
    form_class = forms.SignInForm
    template_name='registration/signin.html'
    redirect_authenticated_user=True