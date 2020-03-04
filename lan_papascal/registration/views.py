from django.shortcuts import render
from django.contrib.auth import views, forms as django_forms
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login as auth_login
)
