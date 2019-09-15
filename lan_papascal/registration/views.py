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
class SignUpView(views.FormView):
    form_class = forms.SignUpForm
    template_name = 'registration/signup.html'
    title = "Sign Up"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs        


class SignInView(views.LoginView):
    form_class = forms.SignInForm
    template_name='registration/signin.html'
    redirect_authenticated_user=True
    title = 'Sign In'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context